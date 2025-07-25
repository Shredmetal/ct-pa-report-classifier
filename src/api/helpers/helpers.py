import csv
import io
import os
import uuid

from src.api.helpers.helpers_config import HelpersConfig


class ApiHelpers:

    @staticmethod
    def validate_csv_content(file_content: bytes) -> bool:
        """Validate that the uploaded file is actually a CSV"""
        try:
            content_str = file_content[:1024].decode('utf-8')
            csv_reader = csv.reader(io.StringIO(content_str))
            next(csv_reader)
            return True
        except (UnicodeDecodeError, csv.Error, StopIteration):
            return False

    @staticmethod
    def secure_filename(filename: str) -> str:
        """Generate a secure filename to prevent directory traversal"""
        base_name = os.path.basename(filename)
        name, ext = os.path.splitext(base_name)
        if ext.lower() not in HelpersConfig.ALLOWED_EXTENSIONS:
            raise ValueError(f"Invalid file extension. Allowed: {HelpersConfig.ALLOWED_EXTENSIONS}")

        # Generate unique filename
        unique_id = str(uuid.uuid4())
        return f"{unique_id}_{name}{ext}"
