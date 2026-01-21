"""Ollama backend module."""

from backends.ollama.backend import OllamaService
from backends.ollama.config import OllamaConfig

__all__ = ["OllamaService", "OllamaConfig"]
