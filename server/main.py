import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .app.api.inference import router as inference_router

from fastapi import FastAPI

app = FastAPI()
app.include_router(inference_router)


@app.get("/")
async def app_root():
    return {
        "status": "OK",
        "response": {
            "content": "Pentagram AI API is running.",
            "version": "1.0.0",
            "author": "Muhammad Bilal Khan",
            "github": "https://github.com/Hi-kue",
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
