# AI Tools - Ollama Assistant

A small Python assistant for local Ollama models with a few practical built-in tools for everyday work.

## Features

- Local Ollama chat
- Direct custom tools for time, system info, shell commands, file listing, and file search
- Simple examples for chat and tool usage
- Configurable model and base URL through environment variables

## Prerequisites

- Python 3.10+
- Ollama installed and running
- A local model installed, for example `qwen2.5-coder:7b`

## Installation

```bash
cd /path/to/ai-tools
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file if you want to override the defaults:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b
```

## Usage

Start Ollama in another terminal:

```bash
ollama run qwen2.5-coder:7b
```

Run the demo script:

```bash
python main.py
```

Or run the examples directly:

```bash
python examples/01_simple_chat.py
python examples/02_custom_tools.py

The chat example includes tool calling. Ask questions like "what time is it" and the assistant can call local tools.
```

## Available Tools

The assistant exposes these local helper tools through Python:

- `get_current_time()`
- `get_system_info()`
- `execute_command(command)`
- `list_files(directory)`
- `search_files(pattern, directory)`
- `count_files(pattern, directory)`

Example:

```python
from src.agent import OllamaAgent

assistant = OllamaAgent()
print(assistant.execute_custom_tool("list_files", directory="."))
```

## Project Structure

```text
ai-tools/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── agent.py
│   └── tools.py
├── examples/
│   ├── 01_simple_chat.py
│   └── 02_custom_tools.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Troubleshooting

If Ollama cannot connect, make sure the model is running and `OLLAMA_BASE_URL` matches your local setup.

If package installation fails on your system Python, recreate the virtual environment with a supported interpreter and install again.
