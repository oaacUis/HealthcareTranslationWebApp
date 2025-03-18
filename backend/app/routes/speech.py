from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from services.speech_service import process_input_audio
from services.speech_service import process_output_audio
import uuid
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DOWNLOAD_DIR = "temp_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@router.post("/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, audio_file.filename)

    try:
        # Save temp file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        # Process the audio file with Whisper
        transcript = process_input_audio(file_path)

        # Remove temp file
        os.remove(file_path)

        return {"transcription": transcript}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="Error during transcription" + str(e))


@router.post("/text-to-speech")
async def text_to_speech(input_text: str):

    try:
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
            detail=f"Error during text-to-speech conversion: {str(e)}")

    print(f"A new audio file was saved successfully at {save_file_path}")

    return FileResponse(save_file_path, media_type="audio/mpeg",
                        filename="output.mp3")
