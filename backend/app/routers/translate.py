from fastapi import APIRouter, HTTPException, Depends
from googletrans import Translator
from pydantic import BaseModel
from auth import get_current_user

router = APIRouter(prefix="/translate", tags=["translate"])
translator = Translator()


# Payload model
class TranslationRequest(BaseModel):
    text: str
    src_lang: str = "auto"  # Detect language automatically by default
    dest_lang: str = "en"  # Translate to English by default


@router.post("/translate")
async def translate_text(request: TranslationRequest,
                         current_user: dict = Depends(get_current_user)):
    """
    Translates the given text from the source language to the destination language.
    Args:
        request (TranslationRequest): The translation request containing the text to be translated,
            the source language code, and the destination language code.
        current_user (dict, optional): The current authenticated user, provided by dependency injection.
    Returns:
        dict: A dictionary containing the original text, the translated text, and the detected source language.
    Raises:
        HTTPException: If an error occurs during the translation process, an HTTP 500 error is raised
            with details about the error.
    """
    try:
        translated = translator.translate(request.text,
                                          src=request.src_lang,
                                          dest=request.dest_lang)

        return {"original_text": request.text,
                "translated_text": translated.text,
                "source_language": translated.src}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Translation error: {str(e)}")
