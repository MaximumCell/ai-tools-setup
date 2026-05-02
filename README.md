# AI Tools - Ollama Agent with CrewAI

A powerful Python framework for creating AI agents powered by your local Ollama models with CrewAI Tools integration. Build intelligent agents that can perform tasks beyond text generation.

## Features

- **Local LLM Integration**: Use Ollama models (Qwen 2.5 Coder, Llama 2, Mistral, etc.)
- **CrewAI Integration**: Build agent teams with defined roles and goals
- **Extensive Tools**:
  - File operations (read, write, delete, directory operations)
  - System commands execution
  - File search and listing
  - System information retrieval
  - Time and date functions
- **Simple Chat Interface**: Direct conversation with your Ollama model
- **Multi-Agent Collaboration**: Create teams of specialized agents
- **Extensible**: Easy to add custom tools and agents

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Ollama model installed (recommended: `qwen2.5-coder`)

### Install Ollama Model

```bash
# Download and run the model
ollama run qwen2.5-coder

# Or use another model
ollama run llama2
ollama run mistral
```

## Installation

1. **Clone/Create the project**

```bash
cd /path/to/ai-tools
```

2. **Create virtual environment** (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

```bash
cp .env.example .env
# Edit .env if needed (defaults work if Ollama is on localhost:11434)
```

## Quick Start

### 1. Start Ollama

In a separate terminal:

```bash
ollama run qwen2.5-coder
```

### 2. Run Examples

**Simple Chat:**

```bash
python examples/01_simple_chat.py
```

**Custom Tools Demo:**

```bash
python examples/02_custom_tools.py
```

**CrewAI Agent:**

```bash
python examples/03_crewai_agent.py
```

**Multi-Agent Collaboration:**

```bash
python examples/04_multi_agent.py
```

**Main Demo:**

```bash
python main.py
```

## Usage Examples

### Simple Chat

```python
from src.agent import SimpleOllamaChat

chat = SimpleOllamaChat()
response = chat.chat("What is Python?")
print(response)
```

### Using Custom Tools

```python
from src.agent import OllamaAgent

agent = OllamaAgent()

# Get current time
time = agent.execute_custom_tool("get_current_time")
print(time)

# List files
files = agent.execute_custom_tool("list_files", directory=".")
print(files)

# Execute command
result = agent.execute_custom_tool("execute_command", command="ls -la")
print(result)
```

### CrewAI Agent with Tasks

```python
from src.agent import OllamaAgent

agent_mgr = OllamaAgent()

# Create agent
agent = agent_mgr.create_agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    backstory="Expert data analyst with years of experience"
)

# Create task
task = agent_mgr.create_task(
    description="Analyze the project structure",
    agent=agent,
    expected_output="Summary of project files and purpose"
)

# Execute
result = agent_mgr.execute([task])
print(result)
```

### Multi-Agent Collaboration

```python
from src.agent import OllamaAgent

agent_mgr = OllamaAgent()

# Create agents
researcher = agent_mgr.create_agent(
    role="Researcher",
    goal="Research and gather information",
    backstory="Thorough researcher"
)

writer = agent_mgr.create_agent(
    role="Writer",
    goal="Write clear documentation",
    backstory="Expert technical writer"
)

# Create tasks
research_task = agent_mgr.create_task(
    description="Research AI trends",
    agent=researcher
)

write_task = agent_mgr.create_task(
    description="Write summary of AI trends",
    agent=writer
)

# Execute
result = agent_mgr.execute([research_task, write_task])
print(result)
```

## Available Tools

### Custom Tools

- `get_current_time()` - Get current date and time
- `get_system_info()` - Get system information
- `execute_command(command)` - Execute shell commands
- `list_files(directory)` - List files in directory
- `search_files(pattern, directory)` - Search for files

### CrewAI Built-in Tools

- `FileReadTool()` - Read file contents
- `FileWriteTool()` - Write to files
- `DirectoryReadTool()` - Read directory contents
- `FileDeleteTool()` - Delete files
- `CodeDocsSearchTool()` - Search code documentation

## Project Structure

```
ai-tools/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration settings
│   ├── agent.py             # Agent implementations
│   ├── tools.py             # Tool definitions
├── examples/
│   ├── 01_simple_chat.py    # Simple chat example
│   ├── 02_custom_tools.py   # Custom tools example
│   ├── 03_crewai_agent.py   # CrewAI agent example
│   ├── 04_multi_agent.py    # Multi-agent example
├── main.py                  # Main entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Configuration

Edit `.env` to customize:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder
```

Or modify `src/config.py` for more advanced settings.

## Troubleshooting

### "Connection refused" Error

- Make sure Ollama is running: `ollama run qwen2.5-coder`
- Check OLLAMA_BASE_URL in `.env` matches your Ollama setup

### Model Not Found

- List installed models: `ollama list`
- Install model: `ollama run qwen2.5-coder`

### ImportError for CrewAI

- Install dependencies: `pip install -r requirements.txt`
- Verify installation: `python -c "import crewai; print(crewai.__version__)"`

### Slow Response Times

- Ensure Ollama is fully loaded before running agents
- Check system resources (CPU/RAM)
- Use a faster model if available (e.g., neural-chat instead of larger models)

## Extending the Framework

### Add Custom Tool

```python
# In src/tools.py

@staticmethod
def my_custom_tool(param1, param2):
    """Description of what your tool does."""
    # Implementation
    return result

# Add to get_custom_tools() function
```

### Add New Agent

```python
from src.agent import OllamaAgent

agent_mgr = OllamaAgent()
new_agent = agent_mgr.create_agent(
    role="Your Role",
    goal="Your Goal",
    backstory="Your Backstory"
)
```

## Switching Models

```bash
# Change in .env or create new chat/agent instance
OLLAMA_MODEL=mistral

# Or in code:
chat = SimpleOllamaChat(model="mistral")
```

## Performance Tips

1. **Use smaller models** for faster responses
2. **Keep Ollama running** between executions
3. **Batch tasks** together when possible
4. **Monitor system resources** during agent execution
5. **Adjust temperature** in config for different behavior

## Supported Ollama Models

- `qwen2.5-coder` - Code generation and analysis
- `mistral` - General purpose
- `neural-chat` - Lightweight and fast
- `llama2` - Powerful and versatile
- `orca-mini` - Small and efficient
- And many more - see [ollama.ai/library](https://ollama.ai/library)

## Contributing

Feel free to fork, modify, and extend this framework for your needs!

## License

MIT License - Feel free to use this in your projects

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama Documentation](https://github.com/jmorganca/ollama)
- [LangChain Documentation](https://python.langchain.com/)

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review example files
3. Check CrewAI and Ollama documentation
4. Review error messages carefully
# ai-tools-setup
