"""RunPod Serverless Handler for Qwen3-TTS"""
import runpod
from engine import get_engine, SPEAKERS, LANGUAGES, DEFAULT_SPEAKER, DEFAULT_LANGUAGE


def handler(job: dict) -> dict:
    """
    RunPod handler function.
    
    Input schema:
    {
        "text": str,              # Required: text to synthesize
        "speaker": str,           # Optional: Vivian, Serena, Uncle_Fu, Dylan, Eric, Ryan, Aiden, Ono_Anna, Sohee
        "instruction": str,       # Optional: style instruction (e.g., "Speak angrily")
        "language": str           # Optional: Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian, Auto
    }

    Output schema:
    {
        "audio_base64": str,      # Base64 encoded WAV
        "sample_rate": int,       # Sample rate (typically 24000)
        "duration_seconds": float
    }
    """
    job_input = job.get("input", {})
    
    # Validate required field
    text = job_input.get("text")
    if not text:
        return {"error": "Missing required field: text"}
    
    # Optional fields with defaults
    speaker = job_input.get("speaker", DEFAULT_SPEAKER)
    instruction = job_input.get("instruction")
    language = job_input.get("language", DEFAULT_LANGUAGE)
    
    print("[Handler] Loading engine...")
    try:
        engine = get_engine()
    except Exception as exc:
        print(f"[Handler] Engine load failed: {exc}")
        raise
    print("[Handler] Engine loaded.")

    print("[Handler] Generating audio...")
    try:
        result = engine.generate(
            text=text,
            speaker=speaker,
            instruction=instruction,
            language=language,
        )
    except Exception as exc:
        print(f"[Handler] Generation failed: {exc}")
        raise
    print("[Handler] Generation complete.")
    return result

runpod.serverless.start({"handler": handler})
