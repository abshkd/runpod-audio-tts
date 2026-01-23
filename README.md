# Qwen3-TTS RunPod Serverless
[![Runpod](https://api.runpod.io/badge/abshkd/runpod-audio-tts)](https://console.runpod.io/hub/abshkd/runpod-audio-tts)
Text-to-Speech endpoint using [Qwen3-TTS-12Hz-1.7B-CustomVoice](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice).

📑 [Qwen3-TTS Documentation](https://github.com/QwenLM/Qwen3-TTS)

## API

### Request

```json
{
  "input": {
    "text": "Hello, this is a test.",
    "speaker": "Ryan",
    "language": "English",
    "instruction": "Speak excitedly"
  }
}
```

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `text` | Yes | - | Text to synthesize |
| `speaker` | No | `Ryan` | Voice ID (see below) |
| `language` | No | `Auto` | Target language |
| `instruction` | No | - | Style control (e.g., "Speak angrily") |

### Response

```json
{
  "audio_base64": "UklGRi...",
  "sample_rate": 24000,
  "duration_seconds": 2.5
}
```

### Speakers

| Speaker | Description |
|---------|-------------|
| Vivian | Bright, slightly edgy young female (Chinese) |
| Serena | Warm, gentle young female (Chinese) |
| Uncle_Fu | Seasoned male, low mellow timbre (Chinese) |
| Dylan | Youthful Beijing male (Chinese-Beijing) |
| Eric | Lively Chengdu male (Chinese-Sichuan) |
| Ryan | Dynamic male, strong rhythmic (English) |
| Aiden | Sunny American male (English) |
| Ono_Anna | Playful Japanese female (Japanese) |
| Sohee | Warm Korean female (Korean) |

### Languages

`Auto`, `Chinese`, `English`, `Japanese`, `Korean`, `German`, `French`, `Russian`, `Portuguese`, `Spanish`, `Italian`

## Examples

### Python

```python
import runpod
import base64

runpod.api_key = "your_api_key"
endpoint = runpod.Endpoint("your_endpoint_id")

result = endpoint.run_sync({
    "input": {
        "text": "Welcome to the future of text to speech.",
        "speaker": "Ryan",
        "language": "English"
    }
})

# Save audio
audio_bytes = base64.b64decode(result["audio_base64"])
with open("output.wav", "wb") as f:
    f.write(audio_bytes)
```

### cURL

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "text": "Hello world!",
      "speaker": "Ryan"
    }
  }'
```

## Development

### Local Testing

```bash
# Build
docker build -t audio-vllm .

# Run locally
docker run --gpus all -e LOCAL_TEST=1 -p 8000:8000 audio-vllm

# Test
curl -X POST http://localhost:8000/runsync \
  -H "Content-Type: application/json" \
  -d '{"input": {"text": "Hello!", "speaker": "Ryan"}}'
```

### Deploy to RunPod

1. Push image to container registry
2. Create Serverless Endpoint with the image
3. Set GPU type (16GB+ VRAM recommended)

## License

Apache-2.0 (follows Qwen3-TTS license)
