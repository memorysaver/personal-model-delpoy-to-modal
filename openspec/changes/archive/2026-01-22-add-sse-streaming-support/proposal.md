# Change: Add SSE Streaming Support

## Why
The current wildcard proxy returns SSE streaming responses as JSON-wrapped strings instead of raw Server-Sent Events. This breaks SDK parsers that expect raw SSE format.

**Root cause:** Modal's `.remote()` is request-response only - it serializes all return values as JSON, breaking SSE streams.

## What Changes
- Add `stream_proxy()` generator method to OllamaService and OllamaBackend
- Use Modal's `.remote_gen()` for streaming requests (documented pattern for GPU → CPU streaming)
- Detect streaming requests (`stream: true` in body) and route differently
- Non-streaming continues using `.remote()` as before

## Impact
- Affected specs: `ollama-deployment` (add streaming requirement)
- Affected code:
  - `serve.py` - Add streaming detection, generator method, modify proxy route
  - `backends/ollama/backend.py` - Add `stream_proxy()` generator to OllamaService

## Architecture

| Request Type | Method | Flow |
|-------------|--------|------|
| Non-streaming | `.remote()` | Gateway → RPC → Backend → Response |
| Streaming | `.remote_gen()` | Gateway → RPC stream → Backend yields → SSE chunks |

This approach maintains CPU/GPU separation while enabling true SSE streaming.
