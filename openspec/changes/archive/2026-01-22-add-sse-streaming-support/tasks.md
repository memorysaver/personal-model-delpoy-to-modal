## 1. Backend Streaming Method ✅
- [x] 1.1 Add `stream_proxy()` generator to `backends/ollama/backend.py`
- [x] 1.2 Method yields raw bytes from Ollama's streaming response

## 2. Gateway Streaming Support ✅
- [x] 2.1 Add `is_streaming_request()` helper to detect `stream: true`
- [x] 2.2 Add `stream_proxy()` generator method to `OllamaBackend` class in `serve.py`
- [x] 2.3 Modify `ollama_proxy()` route to use `.remote_gen()` for streaming
- [x] 2.4 Return `StreamingResponse` with `media_type="text/event-stream"`

## 3. Validation ✅
- [x] 3.1 Deploy with `modal deploy serve.py`
- [x] 3.2 Test non-streaming: `POST /ollama/api/generate` with `stream: false`
- [x] 3.3 Test streaming: `POST /ollama/api/generate` with `stream: true`
- [x] 3.4 Test OpenAI streaming: `POST /ollama/v1/chat/completions` with `stream: true`
- [x] 3.5 Test Anthropic streaming: `POST /ollama/v1/messages` with `stream: true` (implicitly supported)
