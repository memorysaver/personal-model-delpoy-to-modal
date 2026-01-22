## ADDED Requirements

### Requirement: SSE Streaming Support
The gateway SHALL support Server-Sent Events (SSE) streaming for requests with `stream: true`.

#### Scenario: Streaming request detection
- **WHEN** a POST request arrives at `/ollama/*` with `"stream": true` in the body
- **THEN** the gateway routes to the streaming handler
- **AND** uses `.remote_gen()` to stream from the backend generator

#### Scenario: Streaming response format
- **WHEN** a streaming request is processed
- **THEN** the gateway returns `StreamingResponse` with `media_type="text/event-stream"`
- **AND** yields raw bytes from the backend without JSON wrapping
- **AND** sets `Cache-Control: no-cache` and `Connection: keep-alive` headers

#### Scenario: Non-streaming backward compatibility
- **WHEN** a request has `"stream": false` or no `stream` field
- **THEN** the gateway uses `.remote()` (existing behavior)
- **AND** returns `JSONResponse` as before

#### Scenario: Supported streaming endpoints
- **WHEN** streaming is enabled
- **THEN** the following endpoints support SSE:
  - `POST /ollama/api/generate` (native Ollama)
  - `POST /ollama/api/chat` (native Ollama)
  - `POST /ollama/v1/chat/completions` (OpenAI-compatible)
  - `POST /ollama/v1/messages` (Anthropic-compatible)
