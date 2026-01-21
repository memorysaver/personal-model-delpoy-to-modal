## MODIFIED Requirements

### Requirement: Ollama Backend
The system SHALL run Ollama as a GPU-based backend with model persistence.

#### Scenario: Multiple models support
- **WHEN** the OllamaBackend container starts
- **THEN** it pulls all models in the configured list (default: `glm-4.7-flash:q8_0,glm-4.7-flash:q4_K_M`)
- **AND** caches them to the `ollama-models` volume

#### Scenario: Model selection in API calls
- **WHEN** a client sends a request to `/ollama/api/generate` or `/ollama/api/chat`
- **THEN** the client specifies the model via the `model` field in the request body
- **AND** the system uses the specified model for inference
