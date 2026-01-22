"""Global configuration for the Personal Model Garden."""

import os

# App identity
APP_NAME = "personal-model-garden"

# Gateway settings (CPU, always warm)
GATEWAY_MIN_CONTAINERS = int(os.environ.get("GATEWAY_MIN_CONTAINERS", "1"))

# Ollama backend settings (GPU, separate lifecycle)
OLLAMA_GPU = os.environ.get("OLLAMA_GPU", "A10G")
OLLAMA_MAX_CONTAINERS = int(os.environ.get("OLLAMA_MAX_CONTAINERS", "1"))
OLLAMA_SCALEDOWN = int(os.environ.get("OLLAMA_SCALEDOWN", "300"))
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "1800"))

# Diffusers A10G tier settings (24GB VRAM, for smaller models like GLM-Image)
DIFFUSERS_A10G_MAX_CONTAINERS = int(os.environ.get("DIFFUSERS_A10G_MAX_CONTAINERS", "1"))
DIFFUSERS_A10G_SCALEDOWN = int(os.environ.get("DIFFUSERS_A10G_SCALEDOWN", "300"))
DIFFUSERS_A10G_TIMEOUT = int(os.environ.get("DIFFUSERS_A10G_TIMEOUT", "1800"))

# Diffusers L40S tier settings (48GB VRAM, for larger models like SDXL)
DIFFUSERS_L40S_MAX_CONTAINERS = int(os.environ.get("DIFFUSERS_L40S_MAX_CONTAINERS", "1"))
DIFFUSERS_L40S_SCALEDOWN = int(os.environ.get("DIFFUSERS_L40S_SCALEDOWN", "300"))
DIFFUSERS_L40S_TIMEOUT = int(os.environ.get("DIFFUSERS_L40S_TIMEOUT", "1800"))
