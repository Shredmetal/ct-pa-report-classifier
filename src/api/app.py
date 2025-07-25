from fastapi import FastAPI

from src.api.routers.uploader_router import UploaderRouter

app = FastAPI()
app.include_router(UploaderRouter.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)