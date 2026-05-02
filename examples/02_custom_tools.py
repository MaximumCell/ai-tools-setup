"""Example 2: Using custom tools directly."""
import sys
sys.path.insert(0, '..')

from src.agent import OllamaAgent


def main():
    """Run custom tools example."""
    print("Custom Tools Demo")
    print("=" * 50)
    
    agent = OllamaAgent()
    
    # Show available tools
    print("\nAvailable Custom Tools:")
    tools = agent.get_available_tools()
    for i, (tool_name, description) in enumerate(tools.items(), 1):
        print(f"  {i}. {tool_name}: {description}")
    
    # Test tools
    print("\n" + "=" * 50)
    print("Testing Tools:")
    print("=" * 50)
    
    # Get current time
    print("\n1. Current Time:")
    print("-" * 50)
    result = agent.execute_custom_tool("get_current_time")
    print(result)
    
    # Get system info
    print("\n2. System Information:")
    print("-" * 50)
    result = agent.execute_custom_tool("get_system_info")
    print(result)
    
    # List files
    print("\n3. List Files (current directory):")
    print("-" * 50)
    result = agent.execute_custom_tool("list_files", directory=".")
    print(result)
    
    # Search files
    print("\n4. Search Python Files:")
    print("-" * 50)
    result = agent.execute_custom_tool("search_files", pattern="*.py", directory=".")
    print(result)
    
    # Execute command
    print("\n5. Execute Command:")
    print("-" * 50)
    result = agent.execute_custom_tool("execute_command", command="whoami")
    print(f"Current user: {result.strip()}")


if __name__ == "__main__":
    main()
