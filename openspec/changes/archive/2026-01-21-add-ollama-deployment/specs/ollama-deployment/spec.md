## ADDED Requirements

### Requirement: Gateway + Backend Architecture
The system SHALL deploy a CPU-based gateway and GPU-based backends as separate Modal classes with independent lifecycles.

#### Scenario: Gateway always warm
- **WHEN** deploying the system
- **THEN** the gateway runs with `min_containers=1`
- **AND** responds instantly to health checks without triggering backend cold starts

#### Scenario: Backend separate lifecycle
- **WHEN** a request arrives for a backend endpoint
- **THEN** the gateway calls the backend via `@modal.method()` RPC
- **AND** the backend container starts if not already running (cold start)
- **AND** the backend scales down after idle timeout (default: 300s)

### Requirement: Ollama Backend
The system SHALL run Ollama as a GPU-based backend with model persistence.

#### Scenario: Backend startup
- **WHEN** the OllamaBackend container starts
- **THEN** it starts the local Ollama server
- **AND** pulls configured models if not cached
- **AND** commits pulled models to the `ollama-models` volume

#### Scenario: Generate endpoint
- **WHEN** a POST request arrives at `/ollama/api/generate`
- **THEN** the gateway calls `OllamaBackend().generate.remote()`
- **AND** returns the Ollama native response format

#### Scenario: Chat endpoint
- **WHEN** a POST request arrives at `/ollama/api/chat`
- **THEN** the gateway calls `OllamaBackend().chat.remote()`
- **AND** returns the Ollama native response format

#### Scenario: List models endpoint
- **WHEN** a GET request arrives at `/ollama/api/tags`
- **THEN** the gateway calls `OllamaBackend().list_models.remote()`
- **AND** returns the list of available models

### Requirement: Configuration
The system SHALL be configurable via environment variables and config module.

#### Scenario: Gateway configuration
- **WHEN** configuring the gateway
- **THEN** `GATEWAY_MIN_CONTAINERS` controls warm pool size (default: 1)

#### Scenario: Backend configuration
- **WHEN** configuring the Ollama backend
- **THEN** `OLLAMA_GPU` controls GPU type (default: A100-40GB)
- **AND** `OLLAMA_SCALEDOWN` controls idle timeout (default: 300s)
- **AND** `OLLAMA_TIMEOUT` controls request timeout (default: 1800s)

<!-- Note: Original proposal mentioned OpenAI-compatible API, separate directories, and ollama-<model> naming.
     These were descoped in favor of: native Ollama API, unified backends/ structure, and personal-model-garden app name. -->
