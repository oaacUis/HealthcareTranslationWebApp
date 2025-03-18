import whisper
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY is not set in the .env file")

model = whisper.load_model("tiny")


def process_input_audio(file_path):
    result = model.transcribe(file_path)["text"]

    return result


def process_output_audio(input_text):

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    response = client.text_to_speech.convert(
                voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
                optimize_streaming_latency="0",
                output_format="mp3_22050_32",
                text=input_text,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.0,
                    similarity_boost=1.0,
                    style=0.0,
                    use_speaker_boost=True,
                    ),
                )
    return response
