from typing import List, Dict, Any
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.api.routers.processor_router_config import ProcessorRouterConfig
from src.csv_handler.csv_handler import CSVHandler
from src.llm_manager.llm_config import LLMConfig
from src.llm_manager.llm_factory import LLMFactory
from src.llm_tasks.radiology_report_extractor import RadiologyReportStructuredDataExtractor


class ProcessFileRequest(BaseModel):
    filenames: List[str]
    output_prefix: str = "processed_reports"
    llm_base_url: str = ProcessorRouterConfig.LLM_DEFAULT_BASE_URL


class ProcessorRouter:

    router = APIRouter()
    ProcessorRouterConfig.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    @router.post("/api/process-files")
    async def process_files(request: ProcessFileRequest) -> JSONResponse:
        """
        Process a list of CSV files through the radiology report extractor
        """
        try:
            # Validate input
            if not request.filenames:
                raise HTTPException(status_code=400, detail="No filenames provided")

            # Validate files exist and get full paths
            file_paths = []
            missing_files = []

            for filename in request.filenames:
                file_path = ProcessorRouterConfig.SOURCE_DIR / filename
                if not file_path.exists():
                    missing_files.append(filename)
                elif not filename.lower().endswith('.csv'):
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {filename} is not a CSV file"
                    )
                else:
                    file_paths.append(file_path)

            if missing_files:
                raise HTTPException(
                    status_code=404,
                    detail=f"Files not found: {', '.join(missing_files)}"
                )

            # Initialize LLM and extractor
            llm_config = LLMConfig(
                provider=None,
                temperature=0.1,
                max_tokens=4,
                base_url=request.llm_base_url
            )

            llm = LLMFactory.create_llm(llm_config)
            report_extractor = RadiologyReportStructuredDataExtractor(llm)

            # Process each file
            processing_results = []
            total_reports_processed = 0

            for file_path in file_paths:
                try:
                    # Read reports from CSV
                    reports = CSVHandler.read_csv(str(file_path))

                    if not reports:
                        processing_results.append({
                            "filename": file_path.name,
                            "status": "skipped",
                            "message": "No reports found in file",
                            "reports_processed": 0
                        })
                        continue

                    # Generate output paths
                    base_output_name = f"{request.output_prefix}_{file_path.stem}"
                    pe_output_path = ProcessorRouterConfig.OUTPUT_DIR / f"{base_output_name}_pe_data.csv"
                    lung_output_path = ProcessorRouterConfig.OUTPUT_DIR / f"{base_output_name}_lung_abnormality.csv"

                    # Process each report
                    file_reports_processed = 0
                    for report in reports:
                        if report.strip():  # Skip empty reports
                            # Extract PE data
                            pe_data = report_extractor.extract_pe_data(report)
                            CSVHandler.write_to_csv(pe_data, str(pe_output_path), "pe")

                            # Extract lung abnormality data
                            lung_data = report_extractor.extract_lung_abnormality_data(report)
                            CSVHandler.write_to_csv(lung_data, str(lung_output_path), "lung_abnormality")

                            file_reports_processed += 1

                    processing_results.append({
                        "filename": file_path.name,
                        "status": "completed",
                        "reports_processed": file_reports_processed,
                        "pe_output_file": str(pe_output_path),
                        "lung_output_file": str(lung_output_path)
                    })

                    total_reports_processed += file_reports_processed

                except Exception as file_error:
                    processing_results.append({
                        "filename": file_path.name,
                        "status": "failed",
                        "error": str(file_error),
                        "reports_processed": 0
                    })

            # Determine overall status
            failed_files = [r for r in processing_results if r["status"] == "failed"]
            completed_files = [r for r in processing_results if r["status"] == "completed"]

            if failed_files and not completed_files:
                overall_status = "failed"
            elif failed_files and completed_files:
                overall_status = "partial_success"
            else:
                overall_status = "success"

            return JSONResponse(
                status_code=200,
                content={
                    "message": "Processing completed",
                    "overall_status": overall_status,
                    "total_files_processed": len(request.filenames),
                    "total_reports_processed": total_reports_processed,
                    "output_directory": str(ProcessorRouterConfig.OUTPUT_DIR),
                    "file_results": processing_results
                }
            )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    @staticmethod
    @router.get("/api/processed-files")
    async def list_processed_files() -> Dict[str, List[Dict[str, Any]]]:
        """
        List all processed output files
        """
        try:
            if not ProcessorRouterConfig.OUTPUT_DIR.exists():
                return {"files": []}

            output_files = []
            for file_path in ProcessorRouterConfig.OUTPUT_DIR.glob("*.csv"):
                stat = file_path.stat()
                output_files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "path": str(file_path)
                })

            return {"files": output_files}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list processed files: {str(e)}")