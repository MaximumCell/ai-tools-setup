"""Main entry point for the AI Tools assistant."""
from src.agent import OllamaAgent, ToolCallingOllamaChat


def demo_custom_tools():
    """Demo custom tools directly."""
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
    
    chat = ToolCallingOllamaChat()
    
    print("\nMake sure Ollama is running with the qwen2.5-coder:7b model!")
    print("Command: ollama run qwen2.5-coder:7b\n")
    
    # Test simple conversation
    test_prompts = [
        "What is the current date and time?",
        "Tell me about Python",
    ]
    
    for prompt in test_prompts:
        print(f"\n[User]: {prompt}")
        try:
            response = chat.chat_with_tools(prompt)
            print(f"[Ollama]: {response}")
        except Exception as e:
            print(f"[Error]: {str(e)}")
            print("Make sure Ollama is running: ollama run qwen2.5-coder:7b")
            break


def main():
    """Main function."""
    print("\n" + "=" * 60)
    print("AI Tools - Ollama Assistant")
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
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start Ollama: ollama run qwen2.5-coder:7b")
    print("2. Try the examples in the 'examples' directory")
    print("3. Check src/agent.py for implementation details")


if __name__ == "__main__":
    main()
