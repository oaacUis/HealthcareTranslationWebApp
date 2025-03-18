from fastapi import FastAPI
from app.routes.speech import router as speech_router
from app.routes.translate import router as translation_router

app = FastAPI()

# Load routers
app.include_router(speech_router, prefix="/api")
app.include_router(translation_router, prefix="/api")


def main():
    return 0


if __name__ == "__main__":
    main()
