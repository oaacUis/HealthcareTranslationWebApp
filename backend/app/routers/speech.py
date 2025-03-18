from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from services.speech_service import process_input_audio
from services.speech_service import process_output_audio
from auth import get_current_user
import uuid
import shutil
import os

router = APIRouter(prefix="/speech", tags=["speech"])

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DOWNLOAD_DIR = "temp_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@router.post("/speech-to-text")
async def speech_to_text(
    audio_file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
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

        # Process the audio file with Whisper
        transcript = process_input_audio(file_path)

        # Remove temp file
        os.remove(file_path)

        return {"transcription": transcript}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error during transcription" + str(e)
        )


@router.post("/text-to-speech")
async def text_to_speech(
    input_text: str, current_user: dict = Depends(get_current_user)
):
    """
    Converts the given input text into speech and saves the output as an MP3 file.
    Args:
        input_text (str): The text to be converted into speech.
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
