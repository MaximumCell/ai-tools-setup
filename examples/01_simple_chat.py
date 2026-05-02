"""Example 1: Simple chat with Ollama model."""
import sys
sys.path.insert(0, '..')

from src.agent import ToolCallingOllamaChat


def main():
    """Run simple chat example."""
    print("Simple Chat with Ollama")
    print("=" * 50)
    print("\nMake sure Ollama is running:")
    print("  ollama run qwen2.5-coder:7b\n")
    
    chat = ToolCallingOllamaChat()
    
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("\nOllama is thinking...\n")
        response = chat.chat_with_tools(user_input)
        print(f"Assistant: {response}\n")


if __name__ == "__main__":
    main()
