"""Configuration module for AI Tools agent."""
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder")

# Agent configuration
AGENT_CONFIG = {
    "model": OLLAMA_MODEL,
    "base_url": OLLAMA_BASE_URL,
    "verbose": True,
    "temperature": 0.7,
}
