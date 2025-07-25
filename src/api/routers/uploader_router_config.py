from dataclasses import dataclass
from pathlib import Path

from src.api.helpers.helpers_config import HelpersConfig


@dataclass
class UploaderRouterConfig:
    UPLOAD_DIR = Path("data/target")
    MAX_FILE_SIZE = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = HelpersConfig.ALLOWED_EXTENSIONS