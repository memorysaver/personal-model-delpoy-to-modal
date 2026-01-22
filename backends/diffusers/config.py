"""Diffusers backend configuration."""

from dataclasses import dataclass, field


@dataclass
class DiffusersConfig:
    """Configuration for Diffusers backend."""

    # Volume name for HuggingFace cache storage
    volume_name: str = "diffusers-models"

    # Mount path for the volume (HuggingFace default cache location)
    volume_mount: str = "/root/.cache/huggingface"
