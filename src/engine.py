"""TTS Engine wrapper for Qwen3-TTS-12Hz-1.7B-CustomVoice using qwen-tts package"""
import io
import base64
import torch
import soundfile as sf
from typing import Optional

# Model ID (downloaded to HF cache at /models during build)
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"

# Supported speakers for CustomVoice model
SPEAKERS = {
    "Vivian": "Bright, slightly edgy young female (Chinese)",
    "Serena": "Warm, gentle young female (Chinese)",
    "Uncle_Fu": "Seasoned male, low mellow timbre (Chinese)",
    "Dylan": "Youthful Beijing male, clear natural (Chinese-Beijing)",
    "Eric": "Lively Chengdu male, slightly husky (Chinese-Sichuan)",
    "Ryan": "Dynamic male, strong rhythmic (English)",
    "Aiden": "Sunny American male, clear midrange (English)",
    "Ono_Anna": "Playful Japanese female, light nimble (Japanese)",
    "Sohee": "Warm Korean female, rich emotion (Korean)",
}
DEFAULT_SPEAKER = "Ryan"

# Supported languages
LANGUAGES = {"Chinese", "English", "Japanese", "Korean", "German", "French",
             "Russian", "Portuguese", "Spanish", "Italian", "Auto"}
DEFAULT_LANGUAGE = "Auto"


class TTSEngine:
    """Singleton TTS engine using qwen-tts package"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._load_model()

    def _load_model(self):
        """Load the Qwen3-TTS model"""
        from qwen_tts import Qwen3TTSModel

        self.model = Qwen3TTSModel.from_pretrained(
            MODEL_ID,
            device_map="cuda:0",
            dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
        )
        print(f"[TTSEngine] Model loaded: {MODEL_ID}")

    def generate(
        self,
        text: str,
        speaker: str = DEFAULT_SPEAKER,
        instruction: Optional[str] = None,
        language: str = DEFAULT_LANGUAGE,
    ) -> dict:
        """
        Generate speech from text.

        Args:
            text: Text to synthesize
            speaker: Speaker ID (Vivian, Serena, Uncle_Fu, Dylan, Eric, Ryan, Aiden, Ono_Anna, Sohee)
            instruction: Style instruction (optional)
            language: Language code or "Auto"

        Returns:
            dict with audio_base64, sample_rate, duration_seconds
        """
        # Validate speaker
        if speaker not in SPEAKERS:
            speaker = DEFAULT_SPEAKER

        # Validate language
        if language not in LANGUAGES:
            language = DEFAULT_LANGUAGE

        # Generate using qwen-tts API
        kwargs = {
            "text": text,
            "speaker": speaker,
        }

        # Language: pass None or omit for Auto
        if language != "Auto":
            kwargs["language"] = language

        # Instruction (style) is optional
        if instruction:
            kwargs["instruct"] = instruction

        wavs, sr = self.model.generate_custom_voice(**kwargs)

        # Encode to base64 WAV
        audio_base64 = self._encode_audio(wavs[0], sr)
        duration = len(wavs[0]) / sr

        return {
            "audio_base64": audio_base64,
            "sample_rate": sr,
            "duration_seconds": round(duration, 3),
        }

    def _encode_audio(self, audio_data, sample_rate: int) -> str:
        """Encode audio numpy array to base64 WAV string"""
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, sample_rate, format="WAV")
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")

    def get_speakers(self) -> dict:
        """Return available speakers with descriptions"""
        return SPEAKERS.copy()

    def get_languages(self) -> list:
        """Return available languages"""
        return sorted(list(LANGUAGES))


# Module-level singleton getter
_engine: Optional[TTSEngine] = None

def get_engine() -> TTSEngine:
    global _engine
    if _engine is None:
        _engine = TTSEngine()
    return _engine
