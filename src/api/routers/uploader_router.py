import os
from pathlib import Path

from fastapi import UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from src.api.helpers.helpers import ApiHelpers
from src.api.routers.uploader_router_config import UploaderRouterConfig


class UploaderRouter:

    router = APIRouter()
    UploaderRouterConfig.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    @router.post("/api/upload-csv")
    async def upload_csv_file(file: UploadFile = File(...)):
        """
        Upload a CSV file containing radiology reports
        """
        try:
            # Validate file extension
            if not file.filename:
                raise HTTPException(status_code=400, detail="No filename provided")

            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in UploaderRouterConfig.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file type. Only CSV files are allowed."
                )

            # Read file content
            content = await file.read()

            # Check file size
            if len(content) > UploaderRouterConfig.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum size: {UploaderRouterConfig.MAX_FILE_SIZE // (1024 * 1024)}MB"
                )

            # Validate CSV content
            if not ApiHelpers.validate_csv_content(content):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid CSV format"
                )

            # Generate secure filename
            secure_name = ApiHelpers.secure_filename(file.filename)
            file_path = UploaderRouterConfig.UPLOAD_DIR / secure_name

            # Write file to target directory
            with open(file_path, 'wb') as f:
                f.write(content)

            return JSONResponse(
                status_code=201,
                content={
                    "message": "File uploaded successfully",
                    "filename": secure_name,
                    "original_filename": file.filename,
                    "size": len(content),
                    "path": str(file_path)
                }
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    @staticmethod
    @router.get("/api/source-files")
    async def list_source_files():
        """
        List all CSV files in the source directory
        """
        source_dir = Path("data/source")
        if not source_dir.exists():
            return {"files": []}

        csv_files = []
        for file_path in source_dir.glob("*.csv"):
            stat = file_path.stat()
            csv_files.append({
                "filename": file_path.name,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "path": str(file_path)
            })

        return {"files": csv_files}