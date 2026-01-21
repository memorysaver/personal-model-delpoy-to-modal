## 1. Project Structure ✅
- [x] 1.1 Create `backends/` directory with `__init__.py`, `base.py`
- [x] 1.2 Create `backends/ollama/` module with `backend.py`, `config.py`
- [x] 1.3 Create `config/` module with gateway and backend settings
- [x] 1.4 Create `common/` directory for shared types
- [x] 1.5 Create `pyproject.toml` with Modal SDK dependency

## 2. Gateway Implementation ✅
- [x] 2.1 Create `serve.py` with Modal app definition
- [x] 2.2 Define `gateway_image` (CPU, lightweight)
- [x] 2.3 Implement `GatewayServer` class with `@modal.asgi_app()`
- [x] 2.4 Configure `min_containers=1` for always-warm gateway
- [x] 2.5 Add health endpoint and root API info

## 3. Ollama Backend Implementation ✅
- [x] 3.1 Define `ollama_image` with Ollama installation
- [x] 3.2 Implement `OllamaBackend` class with `@modal.enter()` startup
- [x] 3.3 Add `@modal.method()` for: generate, chat, list_models, show_model, embeddings, health
- [x] 3.4 Configure GPU, scaledown, and volume mount
- [x] 3.5 Implement `OllamaService` to manage local Ollama server

## 4. Gateway Routes ✅
- [x] 4.1 Implement `/ollama/api/tags` → `OllamaBackend().list_models.remote()`
- [x] 4.2 Implement `/ollama/api/generate` → `OllamaBackend().generate.remote()`
- [x] 4.3 Implement `/ollama/api/chat` → `OllamaBackend().chat.remote()`
- [x] 4.4 Implement `/ollama/api/show` → `OllamaBackend().show_model.remote()`
- [x] 4.5 Implement `/ollama/api/embed` → `OllamaBackend().embeddings.remote()`
- [x] 4.6 Implement `/ollama/health` → `OllamaBackend().health.remote()`

## 5. Validation ✅
- [x] 5.1 Test locally with `modal serve serve.py`
- [x] 5.2 Verify gateway responds instantly at `/health`
- [x] 5.3 Verify `/ollama/api/tags` triggers backend (cold start on first call)
- [x] 5.4 Test `/ollama/api/generate` with glm-4.7-flash:q8_0
- [x] 5.5 Test `/ollama/api/chat` with chat messages
