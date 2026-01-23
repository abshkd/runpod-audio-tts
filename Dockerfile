# Base: CUDA 12.9 + Python 3.12
FROM nvidia/cuda:12.9.0-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/models
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3-pip \
    git wget curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

WORKDIR /app

# Install deps - qwen-tts is the official package
RUN pip install --no-cache-dir \
    torch \
    qwen-tts \
    runpod \
    soundfile \
    huggingface_hub \
    && pip install --no-cache-dir flash-attn --no-build-isolation

# Download models at build time (to HF cache)
ARG HF_TOKEN=""
ENV HF_TOKEN=${HF_TOKEN}

RUN python -c "from huggingface_hub import snapshot_download; \
snapshot_download('Qwen/Qwen3-TTS-Tokenizer-12Hz'); \
snapshot_download('Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice')"

# Copy source
COPY src/ /app/src/
COPY entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
