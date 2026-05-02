"""Main agent implementation using CrewAI and Ollama."""
import os
import json
from typing import Optional, Dict, Any
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, FileWriteTool, DirectoryReadTool
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, AGENT_CONFIG
from src.tools import CustomTools, get_custom_tools


class OllamaAgent:
    """An AI agent powered by local Ollama model with CrewAI Tools."""

    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        """
        Initialize the Ollama agent.
        
        Args:
            model: Ollama model name (default: qwen2.5-coder)
            base_url: Ollama base URL (default: http://localhost:11434)
        """
        self.model = model
        self.base_url = base_url
        self.custom_tools = CustomTools()
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        """Initialize all available tools for the agent."""
        tools = []
        
        # CrewAI built-in tools
        tools.append(FileReadTool())
        tools.append(FileWriteTool())
        tools.append(DirectoryReadTool())
        
        return tools

    def create_agent(self, role: str, goal: str, backstory: str) -> Agent:
        """
        Create a CrewAI agent.
        
        Args:
            role: Agent's role
            goal: Agent's goal
            backstory: Agent's backstory
            
        Returns:
            Configured Agent instance
        """
        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=self.tools,
            verbose=True,
            # Use Ollama as LLM
            llm=self._get_ollama_llm(),
        )

    def _get_ollama_llm(self):
        """
        Get Ollama LLM instance.
        
        Returns:
            LiteLLM compatible LLM instance
        """
        from langchain_community.llms import Ollama
        
        return Ollama(
            model=self.model,
            base_url=self.base_url,
            temperature=0.7,
        )

    def create_task(self, description: str, agent: Agent, expected_output: str = "") -> Task:
        """
        Create a task for the agent.
        
        Args:
            description: Task description
            agent: Agent to perform the task
            expected_output: Expected output format
            
        Returns:
            Configured Task instance
        """
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output or "Detailed analysis and results",
        )

    def execute(self, tasks: list, agents: list = None) -> str:
        """
        Execute tasks using CrewAI crew.
        
        Args:
            tasks: List of Task objects
            agents: List of Agent objects (if None, agents are extracted from tasks)
            
        Returns:
            Execution result
        """
        crew = Crew(
            agents=agents or [task.agent for task in tasks],
            tasks=tasks,
            verbose=True,
        )
        
        result = crew.kickoff()
        return result

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
        custom_tools_list = get_custom_tools()
        
        tools_info = {
            # CrewAI tools
            "file_read": "Read the contents of a file",
            "file_write": "Write content to a file",
            "directory_read": "Read directory contents",
            # Custom tools
            "get_current_time": "Get current date and time",
            "get_system_info": "Get system information",
            "execute_command": "Execute shell commands",
            "list_files": "List files in a directory",
            "search_files": "Search for files by pattern",
        }
        
        return tools_info


class SimpleOllamaChat:
    """Simple chat interface with Ollama without CrewAI complexity."""
    
    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        """Initialize simple chat."""
        self.model = model
        self.base_url = base_url
        self.llm = self._get_ollama_llm()
        self.conversation_history = []
    
    def _get_ollama_llm(self):
        """Get Ollama LLM instance."""
        from langchain_community.llms import Ollama
        
        return Ollama(
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
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_history(self) -> list:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
