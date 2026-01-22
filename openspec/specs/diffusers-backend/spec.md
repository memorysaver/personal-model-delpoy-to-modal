# diffusers-backend Specification

## Purpose
TBD - created by archiving change add-diffusers-backend. Update Purpose after archive.
## Requirements
### Requirement: Diffusers Backend Architecture
The system SHALL deploy diffusers-based image generation backends as GPU-tiered Modal classes with independent lifecycles.

#### Scenario: Two GPU tier classes
- **WHEN** deploying the diffusers backend
- **THEN** the system creates `DiffusersBackend_A10G` for 24GB VRAM models
- **AND** creates `DiffusersBackend_L40S` for 48GB VRAM models
- **AND** each class has independent scaling and lifecycle configuration

#### Scenario: Backend separate lifecycle
- **WHEN** an image generation request arrives
- **THEN** the gateway routes to the appropriate GPU tier backend via `@modal.method()` RPC
- **AND** the backend container starts if not already running (cold start)
- **AND** the backend scales down after idle timeout (configurable per tier)

### Requirement: Model Registry
The system SHALL maintain an explicit registry mapping model IDs to their pipeline configuration.

#### Scenario: Registry structure
- **WHEN** a model is registered
- **THEN** the registry stores: pipeline class, GPU tier, torch dtype, device map, and default parameters
- **AND** the registry provides lookup by model ID

#### Scenario: Supported models
- **WHEN** the system starts
- **THEN** the following models are registered:
  - `zai-org/GLM-Image` (L40S tier, bfloat16) - requires ~25GB VRAM
  - `stabilityai/stable-diffusion-xl-base-1.0` (L40S tier, float16)

#### Scenario: Unsupported model rejection
- **WHEN** a request specifies a model not in the registry
- **THEN** the gateway returns HTTP 400 with error message listing supported models
- **AND** the GPU backend is NOT awakened

### Requirement: Gateway Model Validation
The gateway SHALL validate model IDs before routing to GPU backends to prevent unnecessary cold starts.

#### Scenario: Model validation at gateway
- **WHEN** a POST request arrives at `/diffusers/generate`
- **THEN** the gateway extracts `model_id` from the request body
- **AND** validates against MODEL_REGISTRY
- **AND** routes to the appropriate GPU tier backend if valid
- **AND** returns 400 error without GPU wake if invalid

#### Scenario: List supported models
- **WHEN** a GET request arrives at `/diffusers/models`
- **THEN** the gateway returns list of supported model IDs with their GPU tier
- **AND** does NOT wake any GPU backend

### Requirement: HuggingFace-Style API
The gateway SHALL expose a HuggingFace Inference API-compatible endpoint for image generation.

#### Scenario: Generate endpoint
- **WHEN** a POST request arrives at `/diffusers/generate`
- **THEN** the request body contains:
  - `model_id` (required): HuggingFace model identifier
  - `inputs` (required): Text prompt for generation
  - `parameters` (optional): Override default generation parameters

#### Scenario: Parameter overrides
- **WHEN** a request includes `parameters` object
- **THEN** the system merges with model defaults
- **AND** supports: `height`, `width`, `num_inference_steps`, `guidance_scale`, `seed`

#### Scenario: Response format
- **WHEN** image generation completes
- **THEN** the response contains raw PNG image bytes
- **AND** the Content-Type header is `image/png`
- **AND** clients can save directly with `curl -o image.png` (HuggingFace Inference API style)

### Requirement: Lazy Model Loading
The backend SHALL load models on first request and cache in memory for subsequent requests.

#### Scenario: First request for model
- **WHEN** the first request arrives for a specific model
- **THEN** the backend loads the pipeline from HuggingFace cache
- **AND** stores the pipeline instance in memory
- **AND** uses the cached instance for subsequent requests

#### Scenario: Memory management
- **WHEN** a model is loaded
- **THEN** only one model pipeline is kept in GPU memory at a time
- **AND** previous model is unloaded if different model requested

### Requirement: Model Persistence
The backend SHALL persist downloaded model weights to Modal volume across container restarts.

#### Scenario: Volume configuration
- **WHEN** the diffusers backend container starts
- **THEN** the `diffusers-models` volume is mounted at `/root/.cache/huggingface`
- **AND** HuggingFace transformers/diffusers use this cache location

#### Scenario: Cache hit on restart
- **WHEN** a container restarts and requests a previously downloaded model
- **THEN** the model loads from volume cache
- **AND** no download from HuggingFace Hub is required

### Requirement: Configuration
The system SHALL be configurable via environment variables for each GPU tier.

#### Scenario: A10G tier configuration
- **WHEN** configuring the A10G diffusers backend
- **THEN** `DIFFUSERS_A10G_MAX_CONTAINERS` controls maximum parallel containers (default: 1)
- **AND** `DIFFUSERS_A10G_SCALEDOWN` controls idle timeout in seconds (default: 300)
- **AND** `DIFFUSERS_A10G_TIMEOUT` controls request timeout in seconds (default: 1800)

#### Scenario: L40S tier configuration
- **WHEN** configuring the L40S diffusers backend
- **THEN** `DIFFUSERS_L40S_MAX_CONTAINERS` controls maximum parallel containers (default: 1)
- **AND** `DIFFUSERS_L40S_SCALEDOWN` controls idle timeout in seconds (default: 300)
- **AND** `DIFFUSERS_L40S_TIMEOUT` controls request timeout in seconds (default: 1800)

