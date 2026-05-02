"""AI Tools package for an Ollama-based assistant."""
from src.agent import OllamaAgent, SimpleOllamaChat
from src.tools import CustomTools, get_custom_tools
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL

__all__ = [
    "OllamaAgent",
    "SimpleOllamaChat",
    "CustomTools",
    "get_custom_tools",
    "OLLAMA_BASE_URL",
    "OLLAMA_MODEL",
]
