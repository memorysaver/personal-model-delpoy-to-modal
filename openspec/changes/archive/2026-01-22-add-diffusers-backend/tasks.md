# Implementation Tasks

## 1. Backend Module Setup
- [x] 1.1 Create `backends/diffusers/__init__.py` with exports
- [x] 1.2 Create `backends/diffusers/config.py` with DiffusersConfig dataclass
- [x] 1.3 Create `backends/diffusers/registry.py` with MODEL_REGISTRY and helper functions

## 2. Diffusers Service Implementation
- [x] 2.1 Create `backends/diffusers/backend.py` with DiffusersService class
- [x] 2.2 Implement lazy model loading with in-memory cache
- [x] 2.3 Implement `generate()` method with parameter merging
- [x] 2.4 Implement `health_check()` method
- [x] 2.5 Add base64 PNG encoding for response

## 3. Global Configuration
- [x] 3.1 Add A10G tier config vars to `config/__init__.py`
- [x] 3.2 Add L40S tier config vars to `config/__init__.py`

## 4. Modal Integration (serve.py)
- [x] 4.1 Create `diffusers_volume` for HuggingFace cache
- [x] 4.2 Create `diffusers_image` with torch/diffusers/transformers
- [x] 4.3 Create `DiffusersBackend_A10G` Modal class
- [x] 4.4 Create `DiffusersBackend_L40S` Modal class

## 5. Gateway Routes
- [x] 5.1 Add `GET /diffusers/models` endpoint (list supported models)
- [x] 5.2 Add `POST /diffusers/generate` endpoint with model validation
- [x] 5.3 Implement GPU tier routing based on model registry

## 6. Validation & Testing
- [x] 6.1 Deploy to Modal and verify cold start
- [x] 6.2 Test GLM-Image generation via API (moved to L40S tier due to VRAM requirements)
- [x] 6.3 Verify unsupported model returns 400 without GPU wake
- [x] 6.4 Verify model persistence across container restart

## Dependencies
- Tasks 1.x can be done in parallel
- Task 2.x depends on 1.x completion
- Task 3.x can be done in parallel with 1.x and 2.x
- Task 4.x depends on 1.x, 2.x, and 3.x
- Task 5.x depends on 4.x
- Task 6.x depends on all above
