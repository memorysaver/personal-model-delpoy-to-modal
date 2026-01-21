"""
Personal Model Garden - Main Gateway

Multi-backend model serving on Modal with a unified FastAPI gateway.
Gateway runs on CPU (always warm), backends run on GPU (separate lifecycle).

Deploy:
    modal deploy serve.py

Serve locally for testing:
    modal serve serve.py
"""

import modal
from fastapi import FastAPI, Request

from config import (
    APP_NAME,
    GATEWAY_MIN_CONTAINERS,
    OLLAMA_GPU,
    OLLAMA_SCALEDOWN,
    OLLAMA_TIMEOUT,
)
from backends.ollama import OllamaService, OllamaConfig

# =============================================================================
# Modal App
# =============================================================================

app = modal.App(APP_NAME)

# Volumes for model storage
ollama_volume = modal.Volume.from_name("ollama-models", create_if_missing=True)

# Backend configurations
ollama_config = OllamaConfig()

# =============================================================================
# Container Images (separate for gateway vs backends)
# =============================================================================

gateway_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("fastapi", "httpx")
    .add_local_python_source("config")
    .add_local_python_source("common")
    .add_local_python_source("backends")
)

ollama_image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("curl", "ca-certificates", "zstd")
    .pip_install("httpx")
    .run_commands(
        f"curl -L https://github.com/ollama/ollama/releases/download/{ollama_config.version}/ollama-linux-amd64.tar.zst -o /tmp/ollama.tar.zst",
        "tar --use-compress-program=unzstd -xf /tmp/ollama.tar.zst -C /usr",
        "rm /tmp/ollama.tar.zst",
    )
    .add_local_python_source("config")
    .add_local_python_source("backends")
)

# =============================================================================
# Ollama Backend (GPU, separate lifecycle)
# =============================================================================


@app.cls(
    image=ollama_image,
    gpu=OLLAMA_GPU,
    volumes={ollama_config.volume_mount: ollama_volume},
    scaledown_window=OLLAMA_SCALEDOWN,
    timeout=OLLAMA_TIMEOUT,
)
class OllamaBackend:
    """Ollama backend running on GPU with separate lifecycle."""

    @modal.enter()
    def start(self):
        """Start Ollama server and pull models on container startup."""
        self.service = OllamaService(ollama_config, volume=ollama_volume)
        self.service.start()

    @modal.method()
    def generate(self, model: str, prompt: str, **kwargs) -> dict:
        """Generate text using Ollama."""
        return self.service.generate(model, prompt, **kwargs)

    @modal.method()
    def chat(self, model: str, messages: list, **kwargs) -> dict:
        """Chat completion using Ollama."""
        return self.service.chat(model, messages, **kwargs)

    @modal.method()
    def list_models(self) -> dict:
        """List available models."""
        return self.service.list_models()

    @modal.method()
    def show_model(self, name: str) -> dict:
        """Show model information."""
        return self.service.show_model(name)

    @modal.method()
    def embeddings(self, model: str, input: str | list[str], **kwargs) -> dict:
        """Generate embeddings."""
        return self.service.embeddings(model, input, **kwargs)

    @modal.method()
    def health(self) -> dict:
        """Health check for the Ollama backend."""
        return self.service.health_check()


# =============================================================================
# FastAPI Gateway
# =============================================================================

gateway = FastAPI(title="Personal Model Garden")


@gateway.get("/health")
async def health():
    """Gateway health check (does not check backends to avoid cold starts)."""
    return {
        "status": "healthy",
        "backends": {
            "ollama": {"status": "available"},
        },
    }


@gateway.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Personal Model Garden",
        "architecture": "Gateway (CPU) + Backends (GPU)",
        "endpoints": {
            "/health": "Gateway health check",
            "/ollama/api/tags": "List Ollama models",
            "/ollama/api/generate": "Generate text (POST)",
            "/ollama/api/chat": "Chat completion (POST)",
            "/ollama/api/show": "Show model info (POST)",
            "/ollama/api/embed": "Generate embeddings (POST)",
            "/ollama/health": "Ollama backend health (triggers cold start)",
        },
    }


# =============================================================================
# Ollama Routes (calls remote OllamaBackend)
# =============================================================================


@gateway.get("/ollama/api/tags")
async def ollama_list_models():
    """List available Ollama models."""
    return OllamaBackend().list_models.remote()


@gateway.post("/ollama/api/generate")
async def ollama_generate(request: Request):
    """Generate text using Ollama."""
    body = await request.json()
    return OllamaBackend().generate.remote(**body)


@gateway.post("/ollama/api/chat")
async def ollama_chat(request: Request):
    """Chat completion using Ollama."""
    body = await request.json()
    return OllamaBackend().chat.remote(**body)


@gateway.post("/ollama/api/show")
async def ollama_show(request: Request):
    """Show model information."""
    body = await request.json()
    return OllamaBackend().show_model.remote(**body)


@gateway.post("/ollama/api/embed")
async def ollama_embed(request: Request):
    """Generate embeddings."""
    body = await request.json()
    return OllamaBackend().embeddings.remote(**body)


@gateway.get("/ollama/health")
async def ollama_health():
    """Check Ollama backend health (will trigger cold start if not running)."""
    return OllamaBackend().health.remote()


# =============================================================================
# Gateway Server (CPU, always warm)
# =============================================================================


@app.cls(
    image=gateway_image,
    min_containers=GATEWAY_MIN_CONTAINERS,
)
class GatewayServer:
    """Main gateway server (CPU, always warm) that routes to backends."""

    @modal.asgi_app()
    def serve(self):
        """Expose the FastAPI gateway."""
        return gateway
