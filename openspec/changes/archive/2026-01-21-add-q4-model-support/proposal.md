# Change: Add glm-4.7-flash:q4_K_M Model Support

## Why
Provide a smaller quantized variant of GLM-4.7-Flash for faster inference and lower memory usage.
Users can choose between q8_0 (higher quality) and q4_K_M (faster/smaller) via the model parameter in API calls.

## What Changes
- Add `glm-4.7-flash:q4_K_M` to the default models list in `backends/ollama/config.py`
- Both models are pulled on backend startup and cached in the volume
- API callers specify which model to use via the `model` field in requests

## Impact
- Affected specs: `ollama-deployment` (add multi-model scenario)
- Affected code:
  - `backends/ollama/config.py` - Update default OLLAMA_MODELS value
