"""Example 3: CrewAI agent with tasks and tools."""
import sys
sys.path.insert(0, '..')

from src.agent import OllamaAgent


def main():
    """Run CrewAI agent example."""
    print("CrewAI Agent Example")
    print("=" * 50)
    print("\nMake sure Ollama is running:")
    print("  ollama run qwen2.5-coder\n")
    
    agent_mgr = OllamaAgent()
    
    try:
        # Create an agent
        print("Creating agent: Code Analyst...")
        agent = agent_mgr.create_agent(
            role="Code Analyst",
            goal="Analyze and understand code files",
            backstory="You are an expert code analyst with deep knowledge of Python and software design patterns."
        )
        
        # Create tasks
        print("Creating task: Analyze Python files...")
        task = agent_mgr.create_task(
            description="Search for Python files in the project and provide a brief analysis of the project structure",
            agent=agent,
            expected_output="List of Python files found and a description of what each file does"
        )
        
        # Execute
        print("\nExecuting crew (this may take a moment)...\n")
        print("=" * 50)
        result = agent_mgr.execute([task])
        print("=" * 50)
        
        print("\nAnalysis Result:")
        print(result)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama run qwen2.5-coder")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check that qwen2.5-coder is installed: ollama list")


if __name__ == "__main__":
    main()
