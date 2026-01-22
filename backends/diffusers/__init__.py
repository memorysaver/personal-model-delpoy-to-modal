"""Diffusers backend for image generation.

Note: DiffusersService is NOT exported here because it requires torch,
which is not installed in the gateway image. Import it directly from
backends.diffusers.backend in GPU backend code.
"""

from backends.diffusers.config import DiffusersConfig
from backends.diffusers.registry import (
    MODEL_REGISTRY,
    get_model_config,
    get_supported_models,
    get_models_by_gpu_tier,
)

__all__ = [
    "DiffusersConfig",
    "MODEL_REGISTRY",
    "get_model_config",
    "get_supported_models",
    "get_models_by_gpu_tier",
]
