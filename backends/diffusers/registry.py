"""Model registry for diffusers pipelines.

Maps model IDs to their pipeline configuration including:
- Pipeline class to use
- GPU tier (a10g or l40s)
- Torch dtype (as string, converted at runtime)
- Default generation parameters
"""

# Registry of supported models
# Key: HuggingFace model ID
# Value: Configuration dict with pipeline info and defaults
# Note: torch_dtype is a string to avoid importing torch in gateway
MODEL_REGISTRY: dict[str, dict] = {
    "zai-org/GLM-Image": {
        "pipeline_class": "GlmImagePipeline",
        "pipeline_module": "diffusers.pipelines.glm_image",
        "gpu_tier": "l40s",  # Requires ~25GB VRAM, too large for A10G (24GB)
        "torch_dtype": "bfloat16",
        "device_map": "cuda",
        "defaults": {
            "height": 1024,
            "width": 1152,
            "num_inference_steps": 30,
            "guidance_scale": 1.5,
        },
    },
    "stabilityai/stable-diffusion-xl-base-1.0": {
        "pipeline_class": "StableDiffusionXLPipeline",
        "pipeline_module": "diffusers",
        "gpu_tier": "l40s",
        "torch_dtype": "float16",
        "device_map": "balanced",
        "defaults": {
            "height": 1024,
            "width": 1024,
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
        },
    },
}


def get_model_config(model_id: str) -> dict | None:
    """Get configuration for a model by ID.

    Args:
        model_id: HuggingFace model identifier

    Returns:
        Model configuration dict or None if not supported
    """
    return MODEL_REGISTRY.get(model_id)


def get_supported_models() -> list[str]:
    """Get list of all supported model IDs.

    Returns:
        List of HuggingFace model identifiers
    """
    return list(MODEL_REGISTRY.keys())


def get_models_by_gpu_tier(tier: str) -> list[str]:
    """Get model IDs that use a specific GPU tier.

    Args:
        tier: GPU tier name ('a10g' or 'l40s')

    Returns:
        List of model IDs for that tier
    """
    return [
        model_id
        for model_id, config in MODEL_REGISTRY.items()
        if config["gpu_tier"] == tier
    ]
