from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.utils.drive_downloader import download_drive_folder
from backend.api import predict_api, history_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FOLDER_URL = "https://drive.google.com/drive/folders/1oqAbBsIjLBqTCGk01CA1WvXwszcY_eLu?usp=sharing"

@asynccontextmanager
async def lifespan(app: FastAPI):
    download_drive_folder(FOLDER_URL, output_dir="AI_ML/models_store")
    yield
    print("Shutting down server...")

app = FastAPI(lifespan=lifespan)

app.include_router(predict_api.router, prefix="/api")
app.include_router(history_api.router, prefix="/api")

# Run with: uvicorn backend.main:app --reload
