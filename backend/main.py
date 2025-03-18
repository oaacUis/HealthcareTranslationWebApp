from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import speech, translate, auth
from app.utils.logger import logger
from app.utils.middleware import middleware_log
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


@app.get("/")
async def root():
    return {"message": "Medical Translation API is running..."}

# To check using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
