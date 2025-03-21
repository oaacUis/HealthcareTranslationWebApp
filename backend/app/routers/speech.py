from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from ..routers.auth import get_current_user
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from openai import OpenAI
import assemblyai as aai
from pydantic import BaseModel
from dotenv import load_dotenv
import uuid
import shutil
import os
from pathlib import Path


router = APIRouter(prefix="/speech", tags=["speech"])

# Set the log file path to the backend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAPI_API_KEY = os.getenv("OPENAPI_API_KEY")
AII_API_KEY = os.getenv("AII_API_KEY")

if not ELEVENLABS_API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY is not set in the .env file")
if not OPENAPI_API_KEY:
    raise RuntimeError("OPENAPI_API_KEY is not set in the .env file")
if not AII_API_KEY:
    raise RuntimeError("AII_API_KEY is not set in the .env file")

UPLOAD_DIR = os.path.join(BASE_DIR, "app/temp", "temp_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DOWNLOAD_DIR = os.path.join(BASE_DIR, "app/temp", "temp_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@router.post("/speech-to-text")
async def speech_to_text(
    use_openai: bool = Form(False),
    language_code: str = Form("es"),
    audio_file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Handles speech-to-text transcription for an uploaded audio file.
    Args:
        audio_file (UploadFile): The audio file to be transcribed, uploaded by the user.
        current_user (dict): The current authenticated user, provided by dependency injection.
    Returns:
        dict: A dictionary containing the transcription of the audio file.
    Raises:
        HTTPException: If an error occurs during the transcription process,
                        an HTTP 500 error is raised with a relevant error message.
    """  # noqa: E501
    file_path = os.path.join(UPLOAD_DIR, audio_file.filename)

    try:
        # Save temp file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        if use_openai:
            file_path = Path(file_path)
            transcript = openai_assistant(file_path)
        else:
            file_path = Path(file_path).as_posix()
            aai.settings.api_key = AII_API_KEY
            transcriber = aai.Transcriber()
            config = aai.TranscriptionConfig(
                        language_code=language_code,
                        speech_model=aai.SpeechModel.nano
                        )

            transcript = transcriber.transcribe(file_path, config=config).text

        # Remove temp file
        os.remove(file_path)

        return {"transcription": transcript}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error during transcription" + str(e) + str(file_path)
        )


def openai_assistant(file_path):
    client = OpenAI(api_key=OPENAPI_API_KEY)
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=file_path, response_format="text").text

    system_prompt = """
    You are a helpful assistant for a health company. Your task is to correct
    any spelling discrepancies in the transcribed text, with special attention
    to medical language. Only add necessary punctuation such as periods,
    commas, and capitalization, and use only the context provided.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content


class TextToSpeech(BaseModel):
    input_text: str


@router.post("/text-to-speech")
async def text_to_speech(
    tts_request: TextToSpeech, current_user: dict = Depends(get_current_user)
):
    """
    Converts the given input text into speech and saves the output as an MP3 file.
    Args:
        input_text (BaseModel): The text to be converted into speech.
        current_user (dict, optional): The current authenticated user,
            provided by the dependency injection of `get_current_user`.
    Returns:
        FileResponse: A response containing the generated MP3 file with the
        appropriate media type and filename.
    Raises:
        HTTPException: If an error occurs during the text-to-speech conversion process.
    Notes:
        - The function generates a unique filename for the output MP3 file and saves it
          in the specified download directory.
        - The `process_output_audio` function is used to process the input text and
          generate the audio chunks.
        - The generated MP3 file is returned as a downloadable file response.
    """  # noqa: E501

    try:
        input_text = tts_request.input_text
        response = process_output_audio(input_text)
        # Generating a unique file name for the output MP3 file
        save_file_path = os.path.join(DOWNLOAD_DIR, f"{uuid.uuid4()}.mp3")

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during text-to-speech conversion: {str(e)}"
        )

    print(f"A new audio file was saved successfully at {save_file_path}")

    return FileResponse(save_file_path, media_type="audio/mpeg",
                        filename="output.mp3")


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
