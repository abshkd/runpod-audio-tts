# Base: CUDA 12.9 + Python 3.12 https://github.com/abshkd/runpod-audio-tts
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

# Install deps
RUN pip install --no-cache-dir \
    torch \
    qwen-tts \
    runpod \
    soundfile \
    huggingface_hub

# Install prebuilt flash-attn (cu12, torch2.9, py3.12)
RUN pip install --no-cache-dir \
    https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.9cxx11abiTRUE-cp312-cp312-linux_x86_64.whl

# Download models at build time (to HF cache)
ARG HF_TOKEN=""
ENV HF_TOKEN=${HF_TOKEN}

RUN python -c "from huggingface_hub import snapshot_download; \
snapshot_download('Qwen/Qwen3-TTS-Tokenizer-12Hz'); \
snapshot_download('Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice')"

# Copy source
COPY handler.py engine.py /

CMD ["python", "/handler.py"]
