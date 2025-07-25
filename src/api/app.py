from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api.routers.misc_router import MiscRouter
from src.api.routers.uploader_router import UploaderRouter
from src.api.routers.processor_router import ProcessorRouter


class DataExtractorApp:

    def __init__(self):
        self.app = FastAPI(title="CT-PA Report Classifier API")
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, replace with specific origins
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.app.include_router(UploaderRouter.router)
        self.app.include_router(ProcessorRouter.router)
        self.app.include_router(MiscRouter.router)

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)