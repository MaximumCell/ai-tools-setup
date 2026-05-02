"""Main entry point for the AI Tools agent."""
import sys
from src.agent import OllamaAgent, SimpleOllamaChat
from src.tools import get_custom_tools


def demo_custom_tools():
    """Demo custom tools directly without CrewAI."""
    print("=" * 60)
    print("DEMO: Custom Tools (Direct Execution)")
    print("=" * 60)
    
    agent = OllamaAgent()
    
    # Test each custom tool
    tools_demo = [
        ("get_current_time", {}),
        ("get_system_info", {}),
        ("list_files", {"directory": "."}),
        ("search_files", {"pattern": "*.py", "directory": "."}),
        ("execute_command", {"command": "echo 'Hello from Ollama Agent!'"}),
    ]
    
    for tool_name, kwargs in tools_demo:
        print(f"\n[Tool: {tool_name}]")
        print(f"Arguments: {kwargs}")
        result = agent.execute_custom_tool(tool_name, **kwargs)
        print(f"Result:\n{result}")


def demo_simple_chat():
    """Demo simple chat interface."""
    print("\n" + "=" * 60)
    print("DEMO: Simple Chat with Ollama")
    print("=" * 60)
    
    chat = SimpleOllamaChat()
    
    print("\nMake sure Ollama is running with the qwen2.5-coder model!")
    print("Command: ollama run qwen2.5-coder\n")
    
    # Test simple conversation
    test_prompts = [
        "What is the current date and time?",
        "Tell me about Python",
    ]
    
    for prompt in test_prompts:
        print(f"\n[User]: {prompt}")
        try:
            response = chat.chat(prompt)
            print(f"[Ollama]: {response}")
        except Exception as e:
            print(f"[Error]: {str(e)}")
            print("Make sure Ollama is running: ollama run qwen2.5-coder")
            break


def demo_crewai_agent():
    """Demo CrewAI agent with tools."""
    print("\n" + "=" * 60)
    print("DEMO: CrewAI Agent with Tools")
    print("=" * 60)
    
    try:
        from crewai import Task
        
        agent_obj = OllamaAgent()
        
        # Create an agent
        agent = agent_obj.create_agent(
            role="System Administrator",
            goal="Help with system tasks and file management",
            backstory="You are a helpful system administrator with access to various tools."
        )
        
        # Create a task
        task = agent_obj.create_task(
            description="List the files in the current directory and provide a summary",
            agent=agent,
            expected_output="A formatted list of files with descriptions"
        )
        
        print("\nExecuting CrewAI task...")
        print("(Make sure Ollama is running!)\n")
        
        result = agent_obj.execute([task])
        print(f"\n[Result]:\n{result}")
        
    except ImportError:
        print("Error: CrewAI not installed yet. Run: pip install crewai")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nMake sure:")
        print("1. Ollama is running: ollama run qwen2.5-coder")
        print("2. Dependencies are installed: pip install -r requirements.txt")


def main():
    """Main function."""
    print("\n" + "=" * 60)
    print("AI Tools - Ollama Agent with CrewAI")
    print("=" * 60)
    
    # Show available tools
    agent = OllamaAgent()
    print("\nAvailable Tools:")
    print("-" * 60)
    tools = agent.get_available_tools()
    for tool_name, description in tools.items():
        print(f"  • {tool_name}: {description}")
    
    # Run demos
    demo_custom_tools()
    demo_simple_chat()
    # Uncomment to test full CrewAI agent (requires Ollama running)
    # demo_crewai_agent()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start Ollama: ollama run qwen2.5-coder")
    print("2. Try the examples in the 'examples' directory")
    print("3. Check src/agent.py for implementation details")


if __name__ == "__main__":
    main()
