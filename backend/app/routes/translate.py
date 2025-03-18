from fastapi import APIRouter, HTTPException
from googletrans import Translator
from pydantic import BaseModel

router = APIRouter()
translator = Translator()


# Payload model
class TranslationRequest(BaseModel):
    text: str
    src_lang: str = "auto"  # Detect language automatically by default
    dest_lang: str = "en"  # Translate to English by default


@router.post("/translate")
async def translate_text(request: TranslationRequest):
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
