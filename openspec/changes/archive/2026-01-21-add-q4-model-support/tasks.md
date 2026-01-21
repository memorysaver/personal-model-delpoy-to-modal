## 1. Configuration Update ✅
- [x] 1.1 Update `backends/ollama/config.py` to include `glm-4.7-flash:q4_K_M` in default models

## 2. Validation ✅
- [x] 2.1 Run `modal serve serve.py` to verify both models are pulled
- [x] 2.2 Test API call with `model: "glm-4.7-flash:q8_0"`
- [x] 2.3 Test API call with `model: "glm-4.7-flash:q4_K_M"`
