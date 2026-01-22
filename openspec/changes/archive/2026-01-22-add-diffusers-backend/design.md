# Design: Diffusers Backend

## Context
The Personal Model Garden currently serves text/chat models via Ollama. This design adds image generation using HuggingFace diffusers library, following the established Gateway + Backend architecture pattern.

**Constraints:**
- Cost-conscious: GPU should only wake when needed
- Different models need different GPU tiers (VRAM requirements vary)
- Modal GPU type is fixed at class definition time (not runtime)
- Follow existing patterns from Ollama backend

## Goals / Non-Goals

**Goals:**
- Support multiple diffusers models via config-driven registry
- Route requests to appropriate GPU tier based on model requirements
- Validate models at gateway level (no GPU wake for unsupported models)
- Cache model weights across container restarts
- HuggingFace-style API (`POST /diffusers/generate`)

**Non-Goals:**
- Training or fine-tuning models
- Image-to-image or inpainting (text-to-image only for v1)
- Automatic GPU tier detection from model metadata

## Decisions

### Decision 1: Two GPU Tier Classes
Create separate Modal classes for each GPU tier rather than a single class.

**Why:** Modal requires GPU type at class definition. Having `DiffusersBackend_A10G` and `DiffusersBackend_L40S` allows routing requests to the appropriate tier based on model requirements.

**Alternatives considered:**
- Single class with largest GPU: Simpler but wasteful ($3+/hr A100 for small models)
- Dynamic class generation: Not supported by Modal's decorator pattern

### Decision 2: Explicit Model Registry
Pre-define supported models with their pipeline class, GPU tier, dtype, and defaults.

```python
MODEL_REGISTRY = {
    "zai-org/GLM-Image": {
        "pipeline_class": GlmImagePipeline,
        "gpu_tier": "l40s",  # Requires ~25GB VRAM, too large for A10G (24GB)
        "torch_dtype": "bfloat16",
        "defaults": {"height": 1024, "width": 1152, ...}
    },
    ...
}
```

**Why:**
- Different pipelines have different APIs and parameters
- GPU requirements vary significantly (8GB vs 48GB)
- Provides predictable, tested behavior
- Gateway can validate without GPU wake

**Alternatives considered:**
- Auto-detect from HuggingFace: Unpredictable for unknown models
- Full config file (YAML): Over-engineered for personal use

### Decision 3: Lazy Model Loading with In-Memory Cache
Load models on first request, cache in memory for subsequent requests.

**Why:**
- Faster container cold start (no eager loading)
- Multiple models can be used without pre-loading all
- Memory-efficient (only loads what's needed)

### Decision 4: Modal Volume for HuggingFace Cache
Mount volume at `/root/.cache/huggingface` to persist downloaded models.

**Why:**
- Diffusers models are large (5-15GB each)
- Re-downloading on every cold start wastes time/bandwidth
- Follows Ollama backend pattern

### Decision 5: HuggingFace-Style API
Use `POST /diffusers/generate` with `model_id` and `inputs` fields.

```json
{
  "model_id": "zai-org/GLM-Image",
  "inputs": "A sunset over mountains",
  "parameters": {"height": 1024, "width": 1152}
}
```

**Why:** Familiar to HF users, consistent with HF Inference API conventions.

### Decision 6: Raw PNG Response (HuggingFace Style)
Return generated images as raw PNG bytes with `Content-Type: image/png`.

```bash
# Simple usage - save directly to file
curl -X POST "url/diffusers/generate" \
  -H "Content-Type: application/json" \
  -d '{"model_id": "...", "inputs": "..."}' \
  -o image.png
```

**Why:**
- Matches HuggingFace Inference API style
- No 33% size overhead from base64 encoding
- No JSON parsing issues with large payloads
- Direct streaming support
- Simpler client code

**Changed from original design:** Originally planned base64 JSON response, but switched to raw bytes after testing showed large base64 strings could break some clients.

## Architecture

```
Request Flow:

Client ─── POST /diffusers/generate ──► Gateway (CPU)
                                            │
                                  Parse model_id
                                            │
                              Lookup MODEL_REGISTRY
                                   /              \
                            Not found          Found
                                │                  │
                         400 Error           Get gpu_tier
                      (no GPU wake)               │
                                           ┌─────┴─────┐
                                        a10g          l40s
                                           │              │
                              DiffusersBackend_A10G    DiffusersBackend_L40S
                                           │              │
                                      Lazy load pipeline
                                           │
                                      Generate image
                                           │
                                   Return raw PNG bytes
```

## File Structure

```
backends/
├── diffusers/
│   ├── __init__.py          # Exports + registration
│   ├── config.py            # DiffusersConfig dataclass
│   ├── registry.py          # MODEL_REGISTRY mapping
│   └── backend.py           # DiffusersService class

serve.py additions:
├── diffusers_volume         # Modal volume for HF cache
├── diffusers_config         # Config instance
├── diffusers_image          # Container image with torch/diffusers
├── DiffusersBackend_A10G    # Modal class for A10G tier
├── DiffusersBackend_L40S    # Modal class for L40S tier
└── /diffusers/generate      # Gateway route

config/__init__.py additions:
├── DIFFUSERS_A10G_MAX_CONTAINERS
├── DIFFUSERS_A10G_SCALEDOWN
├── DIFFUSERS_A10G_TIMEOUT
├── DIFFUSERS_L40S_MAX_CONTAINERS
├── DIFFUSERS_L40S_SCALEDOWN
└── DIFFUSERS_L40S_TIMEOUT
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Large container image (~10GB with PyTorch) | Use slim base, only install required packages |
| Long first-request latency (model load) | Accept for personal use; could add warm-up endpoint later |
| VRAM exhaustion with multiple models | Lazy loading + single model at a time; document limits |
| Pipeline API differences | Registry stores pipeline class; service handles initialization |

## Open Questions
None - design decisions made during brainstorming session with user.
