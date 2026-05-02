"""Example 4: Multi-agent collaboration."""
import sys
sys.path.insert(0, '..')

from src.agent import OllamaAgent


def main():
    """Run multi-agent example."""
    print("Multi-Agent Collaboration Example")
    print("=" * 50)
    print("\nMake sure Ollama is running:")
    print("  ollama run qwen2.5-coder\n")
    
    agent_mgr = OllamaAgent()
    
    try:
        # Create multiple agents
        print("Creating agents...\n")
        
        researcher = agent_mgr.create_agent(
            role="Research Analyst",
            goal="Research and gather information about topics",
            backstory="You are a thorough researcher who gathers comprehensive information."
        )
        
        writer = agent_mgr.create_agent(
            role="Technical Writer",
            goal="Write clear and concise technical documentation",
            backstory="You are an expert technical writer who creates clear, organized documentation."
        )
        
        # Create tasks
        print("Creating tasks...\n")
        
        research_task = agent_mgr.create_task(
            description="Research what CrewAI is and its main features",
            agent=researcher,
            expected_output="A comprehensive overview of CrewAI"
        )
        
        write_task = agent_mgr.create_task(
            description="Based on the research, write a brief introduction to CrewAI for beginners",
            agent=writer,
            expected_output="A clear and beginner-friendly introduction to CrewAI"
        )
        
        # Execute
        print("Executing multi-agent crew...\n")
        print("=" * 50)
        result = agent_mgr.execute([research_task, write_task], agents=[researcher, writer])
        print("=" * 50)
        
        print("\nFinal Output:")
        print(result)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running with qwen2.5-coder")


if __name__ == "__main__":
    main()
