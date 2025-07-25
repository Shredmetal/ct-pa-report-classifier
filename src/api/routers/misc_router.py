import os
from pathlib import Path
from typing import List, Dict, Any
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from src.api.routers.misc_router_config import MiscRouterConfig


class DeleteFileRequest(BaseModel):
    filenames: List[str]
    directory: str  # "source" or "output"


class MiscRouter:
    router = APIRouter()

    @staticmethod
    def _validate_directory(directory: str) -> Path:
        """Validate and return the directory path"""
        if directory not in MiscRouterConfig.ALLOWED_DIRECTORIES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid directory. Allowed: {list(MiscRouterConfig.ALLOWED_DIRECTORIES.keys())}"
            )
        return MiscRouterConfig.ALLOWED_DIRECTORIES[directory]

    @staticmethod
    def _validate_file_path(filename: str, base_dir: Path) -> Path:
        """Validate file path and prevent directory traversal"""
        # Remove any path separators to prevent directory traversal
        safe_filename = os.path.basename(filename)
        file_path = base_dir / safe_filename

        # Ensure the resolved path is still within the base directory
        try:
            file_path.resolve().relative_to(base_dir.resolve())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file path: {filename}"
            )

        return file_path

    @staticmethod
    @router.delete("/api/delete-files")
    async def delete_files(request: DeleteFileRequest):
        """
        Delete files from specified directory (source or output)
        """
        try:
            # Validate input
            if not request.filenames:
                raise HTTPException(status_code=400, detail="No filenames provided")

            # Validate directory
            target_dir = MiscRouter._validate_directory(request.directory)

            # Process each file
            deletion_results = []
            successful_deletions = 0

            for filename in request.filenames:
                try:
                    # Validate and get file path
                    file_path = MiscRouter._validate_file_path(filename, target_dir)

                    # Check if file exists
                    if not file_path.exists():
                        deletion_results.append({
                            "filename": filename,
                            "status": "not_found",
                            "message": "File does not exist"
                        })
                        continue

                    # Check if it's actually a file (not a directory)
                    if not file_path.is_file():
                        deletion_results.append({
                            "filename": filename,
                            "status": "failed",
                            "message": "Path is not a file"
                        })
                        continue

                    # Delete the file
                    file_path.unlink()
                    deletion_results.append({
                        "filename": filename,
                        "status": "deleted",
                        "message": "File deleted successfully"
                    })
                    successful_deletions += 1

                except HTTPException:
                    raise
                except Exception as file_error:
                    deletion_results.append({
                        "filename": filename,
                        "status": "failed",
                        "message": f"Deletion failed: {str(file_error)}"
                    })

            # Determine overall status
            failed_deletions = [r for r in deletion_results if r["status"] == "failed"]
            not_found_files = [r for r in deletion_results if r["status"] == "not_found"]

            if successful_deletions == 0:
                if failed_deletions:
                    overall_status = "failed"
                else:
                    overall_status = "no_files_found"
            elif failed_deletions or not_found_files:
                overall_status = "partial_success"
            else:
                overall_status = "success"

            return JSONResponse(
                status_code=200,
                content={
                    "message": "Deletion operation completed",
                    "overall_status": overall_status,
                    "directory": request.directory,
                    "total_files_requested": len(request.filenames),
                    "successful_deletions": successful_deletions,
                    "file_results": deletion_results
                }
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Deletion operation failed: {str(e)}")

    @staticmethod
    @router.get("/api/list-files/{directory}")
    async def list_files_by_directory(directory: str):
        """
        List files in specified directory (source or output)
        """
        try:
            # Validate directory
            target_dir = MiscRouter._validate_directory(directory)

            if not target_dir.exists():
                return {
                    "directory": directory,
                    "files": []
                }

            files = []
            for file_path in target_dir.iterdir():
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        "filename": file_path.name,
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                        "path": str(file_path)
                    })

            return {
                "directory": directory,
                "files": files
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

    @staticmethod
    @router.delete("/api/clear-directory/{directory}")
    async def clear_directory(directory: str):
        """
        Delete all files in specified directory (source or output)
        """
        try:
            # Validate directory
            target_dir = MiscRouter._validate_directory(directory)

            if not target_dir.exists():
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Directory does not exist",
                        "directory": directory,
                        "files_deleted": 0
                    }
                )

            # Get all files in directory
            files_to_delete = [f for f in target_dir.iterdir() if f.is_file()]

            if not files_to_delete:
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Directory is already empty",
                        "directory": directory,
                        "files_deleted": 0
                    }
                )

            # Delete all files
            deleted_count = 0
            failed_deletions = []

            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    failed_deletions.append({
                        "filename": file_path.name,
                        "error": str(e)
                    })

            response_data = {
                "message": f"Directory clearing completed",
                "directory": directory,
                "files_deleted": deleted_count,
                "total_files": len(files_to_delete)
            }

            if failed_deletions:
                response_data["failed_deletions"] = failed_deletions
                response_data["status"] = "partial_success"
            else:
                response_data["status"] = "success"

            return JSONResponse(status_code=200, content=response_data)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to clear directory: {str(e)}")

    @staticmethod
    @router.get("/api/download-file/{directory}/{filename}")
    async def download_file(directory: str, filename: str):
        """
        Download a file from specified directory (source or output)
        """
        try:
            # Validate directory
            target_dir = MiscRouter._validate_directory(directory)
            
            # Validate and get file path
            file_path = MiscRouter._validate_file_path(filename, target_dir)
            
            # Check if file exists
            if not file_path.exists():
                raise HTTPException(
                    status_code=404,
                    detail=f"File '{filename}' not found in {directory} directory"
                )
            
            # Check if it's actually a file
            if not file_path.is_file():
                raise HTTPException(
                    status_code=400,
                    detail=f"'{filename}' is not a file"
                )
            
            # Return file for download
            return FileResponse(
                path=str(file_path),
                filename=filename,
                media_type='application/octet-stream'
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")