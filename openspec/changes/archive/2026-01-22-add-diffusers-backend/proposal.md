# Change: Add Diffusers Backend for Image Generation

**Status: IMPLEMENTED** ✅

## Why
The current system only supports text generation via the Ollama backend. Adding a diffusers-based backend enables image generation capabilities using models like GLM-Image, Stable Diffusion XL, and other HuggingFace diffusion models, expanding the platform's utility for personal ML experiments.

## What Changes
- Add new `backends/diffusers/` module with model registry, config, and backend classes
- Add two GPU-tiered Modal classes: `DiffusersBackend_A10G` and `DiffusersBackend_L40S`
- Add gateway route `/diffusers/generate` with model validation (rejects unsupported models without GPU wake)
- Add Modal volume `diffusers-models` for HuggingFace cache persistence
- Add global config variables for diffusers backend settings

## Implementation Notes (Post-Design Changes)

### GPU Tier Adjustment
- GLM-Image moved from A10G (24GB) to L40S (48GB) tier
- Reason: Model requires ~25GB VRAM during inference, exceeds A10G capacity

### Response Format Change
- Changed from JSON with base64-encoded images to raw PNG bytes
- Reason: Large base64 strings can break some clients; matches HuggingFace Inference API style
- Usage: `curl ... -o image.png` (direct save, no JSON parsing needed)

## Impact
- Affected specs: New `diffusers-backend` capability
- Affected code:
  - `backends/diffusers/` (new)
  - `serve.py` (add diffusers route and backend classes)
  - `config/__init__.py` (add diffusers config vars)
- No breaking changes to existing Ollama functionality
