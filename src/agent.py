"""Ollama chat interface and local helper tools."""
from typing import Dict, Optional
import json
import re
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from src.tools import get_custom_tools


class SimpleOllamaChat:
    """Simple chat interface with Ollama."""

    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        """
        Initialize the Ollama chat client.
        
        Args:
            model: Ollama model name (default: qwen2.5-coder)
            base_url: Ollama base URL (default: http://localhost:11434)
        """
        self.model = model
        self.base_url = base_url
        self.llm = self._get_ollama_llm()
        self.conversation_history = []

    def _get_ollama_llm(self):
        """
        Get Ollama LLM instance.
        
        Returns:
            ChatOllama instance
        """
        from langchain_community.chat_models import ChatOllama
        
        return ChatOllama(
            model=self.model,
            base_url=self.base_url,
            temperature=0.7,
        )

    def chat(self, message: str) -> str:
        """
        Send a message and get a response.
        
        Args:
            message: User message
            
        Returns:
            Model response
        """
        self.conversation_history.append({"role": "user", "content": message})

        try:
            response = self.llm.invoke(message)
            response_text = getattr(response, "content", response)
            self.conversation_history.append({"role": "assistant", "content": response_text})
            return response_text
        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self) -> list:
        """Get conversation history."""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []


class OllamaAgent(SimpleOllamaChat):
    """Local Ollama assistant with custom tools."""

    def execute_custom_tool(self, tool_name: str, **kwargs) -> str:
        """
        Execute a custom tool directly.
        
        Args:
            tool_name: Name of the custom tool
            **kwargs: Tool arguments
            
        Returns:
            Tool result
        """
        custom_tools = get_custom_tools()
        
        if tool_name not in custom_tools:
            return f"Tool '{tool_name}' not found. Available tools: {', '.join(custom_tools.keys())}"
        
        try:
            tool_func = custom_tools[tool_name]
            return tool_func(**kwargs)
        except TypeError as e:
            return f"Error calling tool '{tool_name}': {str(e)}"
        except Exception as e:
            return f"Error executing tool: {str(e)}"

    def get_available_tools(self) -> Dict[str, str]:
        """
        Get information about available tools.
        
        Returns:
            Dictionary of tool names and descriptions
        """
        tools_info = {
            # Custom tools
            "get_current_time": "Get current date and time",
            "get_system_info": "Get system information",
            "execute_command": "Execute shell commands",
            "list_files": "List files in a directory",
            "search_files": "Search for files by pattern",
            "count_files": "Count files by pattern",
        }
        
        return tools_info


class ToolCallingOllamaChat(OllamaAgent):
    """Chat interface that can call local tools."""

    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        super().__init__(model=model, base_url=base_url)
        self._messages = [self._build_system_message()]

    def _build_system_message(self):
        from langchain_core.messages import SystemMessage

        tools = self.get_available_tools()
        tool_lines = [f"- {name}: {desc}" for name, desc in tools.items()]
        prompt = (
            "You are a local assistant with tool access. "
            "When a tool is needed, respond with JSON only: "
            "{\"tool\": \"tool_name\", \"args\": {}}. "
            "When replying to the user, respond with JSON only: "
            "{\"final\": \"your response\"}. "
            "Do not include markdown or extra text.\n\n"
            "Examples:\n"
            "User: what time is it\n"
            "Assistant: {\"tool\": \"get_current_time\", \"args\": {}}\n"
            "User: list files in current directory\n"
            "Assistant: {\"tool\": \"list_files\", \"args\": {\"directory\": \".\"}}\n"
            "User: how many py files are in my folder\n"
            "Assistant: {\"tool\": \"count_files\", \"args\": {\"pattern\": "*.py", \"directory\": "."}}\n\n"
            "Available tools:\n"
            + "\n".join(tool_lines)
        )
        return SystemMessage(content=prompt)

    def _parse_json(self, text: str) -> Optional[dict]:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(json)?\s*|```$", "", cleaned, flags=re.IGNORECASE).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    return None
        return None

    def _infer_tool_call(self, message: str) -> Optional[dict]:
        lowered = message.lower()

        if any(kw in lowered for kw in ["time", "date"]):
            return {"tool": "get_current_time", "args": {}}

        if "system info" in lowered or "system information" in lowered:
            return {"tool": "get_system_info", "args": {}}

        if "how many" in lowered and "py" in lowered:
            return {"tool": "count_files", "args": {"pattern": "*.py", "directory": "."}}

        if "list" in lowered and "file" in lowered:
            return {"tool": "list_files", "args": {"directory": "."}}

        if "search" in lowered and "file" in lowered:
            return {"tool": "search_files", "args": {"pattern": "*", "directory": "."}}

        if lowered.startswith("cat "):
            return {"tool": "execute_command", "args": {"command": lowered}}

        if "run" in lowered and "shell" in lowered:
            return {"tool": "execute_command", "args": {"command": message}}

        return None

    def chat_with_tools(self, message: str, max_steps: int = 4) -> str:
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

        self._messages.append(HumanMessage(content=message))

        inferred_once = False

        for _ in range(max_steps):
            response = self.llm.invoke(self._messages)
            content = getattr(response, "content", str(response))
            self._messages.append(AIMessage(content=content))

            payload = self._parse_json(content)
            if not payload:
                inferred = self._infer_tool_call(message)
                if inferred and not inferred_once:
                    inferred_once = True
                    tool_name = inferred.get("tool", "")
                    args = inferred.get("args", {})
                    return self.execute_custom_tool(tool_name, **args)
                return content

            if "tool" in payload:
                tool_name = payload.get("tool", "")
                args = payload.get("args", {})
                tool_result = self.execute_custom_tool(tool_name, **args)
                tool_message = SystemMessage(
                    content=f"Tool result for {tool_name}: {tool_result}"
                )
                self._messages.append(tool_message)
                continue

            if "final" in payload:
                return str(payload.get("final", ""))

        return "Error: tool loop exceeded max steps"
