from fastapi import FastAPI
import uvicorn

from src.api.routers.uploader_router import UploaderRouter
from src.api.routers.processor_router import ProcessorRouter


class DataExtractorApp:

    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(UploaderRouter.router)
        self.app.include_router(ProcessorRouter.router)

    def run(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)