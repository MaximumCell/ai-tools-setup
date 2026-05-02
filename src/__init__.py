"""AI Tools package for Ollama agent with CrewAI."""
from src.agent import OllamaAgent, SimpleOllamaChat
from src.tools import CustomTools, get_crewai_tools, get_custom_tools
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL

__all__ = [
    "OllamaAgent",
    "SimpleOllamaChat",
    "CustomTools",
    "get_crewai_tools",
    "get_custom_tools",
    "OLLAMA_BASE_URL",
    "OLLAMA_MODEL",
]
