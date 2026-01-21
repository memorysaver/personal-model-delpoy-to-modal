"""Ollama backend configuration."""

import os
from dataclasses import dataclass, field


@dataclass
class OllamaConfig:
    """Configuration for Ollama backend."""

    # Models to serve (pulled on startup if not cached)
    models: list[str] = field(
        default_factory=lambda: os.environ.get(
            "OLLAMA_MODELS", "glm-4.7-flash:q8_0,glm-4.7-flash:q4_K_M"
        ).split(",")
    )

    # Ollama version to install
    version: str = field(
        default_factory=lambda: os.environ.get("OLLAMA_VERSION", "v0.14.3-rc3")
    )

    # Port Ollama listens on
    port: int = 11434

    # Volume name for model storage
    volume_name: str = "ollama-models"

    # Mount path for the volume
    volume_mount: str = "/root/.ollama"
