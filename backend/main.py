from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import speech, translate, auth
from app.utils.logger import logger
from app.utils.middleware import middleware_log
from app.database import engine, Base
import asyncio
import uvicorn


app = FastAPI(
    title="Medical Translation API",
    description="Web-based prototype that enables multilingual translation\
        between patients and healthcare providers.",
    version="1.0.0"
)

app.middleware("http")(middleware_log)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Could be restricted to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers from modules
app.include_router(auth.router)
app.include_router(speech.router)
app.include_router(translate.router)

logger.info("Starting API...")

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Medical Translation API is running..."}

@app.get("/home")
async def home():
    """
    Endpoint for the home page.

    Returns:
        dict: A dict containing the health check status and model version.
    """
    await asyncio.sleep(0)  # type: ignore
    API_version = "1.0.0"
    return {"health_check": "OK", "API_version": API_version}

# To check using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
