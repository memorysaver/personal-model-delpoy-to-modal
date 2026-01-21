# Change: Personal Model Garden with Gateway + Backend Architecture

## Why
Enable personal inference of models via a unified gateway that routes to GPU backends.
The gateway stays warm for instant responses while backends scale independently.

## What Changes
- Unified `serve.py` with Gateway (CPU) + OllamaBackend (GPU) classes
- `backends/ollama/` module with `OllamaService` for managing local Ollama server
- `config/` module for centralized configuration
- Gateway uses `@modal.method()` RPC to call backends, not localhost proxy

## Impact
- Affected specs: `ollama-deployment` (rewritten for gateway architecture)
- Affected code:
  - `serve.py` - Gateway and backend definitions
  - `backends/ollama/backend.py` - OllamaService with RPC methods
  - `backends/ollama/config.py` - Ollama-specific config
  - `backends/base.py` - Abstract backend interface
  - `config/__init__.py` - Global config (APP_NAME, GPU settings)
