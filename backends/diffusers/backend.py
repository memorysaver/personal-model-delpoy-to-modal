"""Diffusers backend service for image generation."""

import importlib
from io import BytesIO

import torch

from backends.base import BaseBackend
from backends.diffusers.config import DiffusersConfig
from backends.diffusers.registry import get_model_config


def _get_torch_dtype(dtype_str: str):
    """Convert string dtype to torch dtype.

    Args:
        dtype_str: String representation of dtype (e.g., 'float16', 'bfloat16')

    Returns:
        Corresponding torch dtype
    """
    dtype_map = {
        "float16": torch.float16,
        "float32": torch.float32,
        "bfloat16": torch.bfloat16,
    }
    return dtype_map.get(dtype_str, torch.float16)


class DiffusersService(BaseBackend):
    """Service for generating images using HuggingFace diffusers pipelines.

    Implements lazy model loading - pipelines are loaded on first request
    and cached in memory for subsequent requests.
    """

    name = "diffusers"

    def __init__(self, config: DiffusersConfig):
        """Initialize the diffusers service.

        Args:
            config: Diffusers configuration
        """
        self.config = config
        self._current_model_id: str | None = None
        self._pipeline = None

    def start(self) -> None:
        """Start the service (no-op for lazy loading)."""
        pass

    def health_check(self) -> dict:
        """Return health status.

        Returns:
            Dict with status and loaded model info
        """
        return {
            "status": "healthy",
            "loaded_model": self._current_model_id,
        }

    def _load_pipeline(self, model_id: str) -> None:
        """Load a pipeline for the given model.

        If a different model is already loaded, it will be unloaded first.

        Args:
            model_id: HuggingFace model identifier
        """
        if self._current_model_id == model_id and self._pipeline is not None:
            return

        # Unload previous model if different
        if self._pipeline is not None:
            del self._pipeline
            self._pipeline = None
            torch.cuda.empty_cache()

        model_config = get_model_config(model_id)
        if model_config is None:
            raise ValueError(f"Unsupported model: {model_id}")

        # Dynamically import the pipeline class
        module = importlib.import_module(model_config["pipeline_module"])
        pipeline_class = getattr(module, model_config["pipeline_class"])

        # Convert string dtype to torch dtype
        torch_dtype = _get_torch_dtype(model_config["torch_dtype"])

        # Load the pipeline
        self._pipeline = pipeline_class.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            device_map=model_config["device_map"],
        )

        self._current_model_id = model_id

    def generate(
        self,
        model_id: str,
        prompt: str,
        height: int | None = None,
        width: int | None = None,
        num_inference_steps: int | None = None,
        guidance_scale: float | None = None,
        seed: int | None = None,
    ) -> bytes:
        """Generate an image from a text prompt.

        Args:
            model_id: HuggingFace model identifier
            prompt: Text prompt for generation
            height: Image height (uses model default if not specified)
            width: Image width (uses model default if not specified)
            num_inference_steps: Number of denoising steps
            guidance_scale: Guidance scale for generation
            seed: Random seed for reproducibility

        Returns:
            Raw PNG image bytes (HuggingFace Inference API style)
        """
        model_config = get_model_config(model_id)
        if model_config is None:
            raise ValueError(f"Unsupported model: {model_id}")

        # Load pipeline (lazy loading)
        self._load_pipeline(model_id)

        # Merge parameters with defaults
        defaults = model_config["defaults"]
        params = {
            "prompt": prompt,
            "height": height if height is not None else defaults.get("height", 1024),
            "width": width if width is not None else defaults.get("width", 1024),
            "num_inference_steps": (
                num_inference_steps
                if num_inference_steps is not None
                else defaults.get("num_inference_steps", 30)
            ),
            "guidance_scale": (
                guidance_scale
                if guidance_scale is not None
                else defaults.get("guidance_scale", 7.5)
            ),
        }

        # Add generator with seed if specified
        if seed is not None:
            params["generator"] = torch.Generator(device="cuda").manual_seed(seed)

        # Generate image
        result = self._pipeline(**params)
        image = result.images[0]

        # Return raw PNG bytes (HuggingFace Inference API style)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()
