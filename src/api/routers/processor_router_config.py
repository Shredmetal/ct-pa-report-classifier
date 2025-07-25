from dataclasses import dataclass
from pathlib import Path

from src.api.helpers.helpers_config import HelpersConfig


@dataclass
class ProcessorRouterConfig:
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
    SOURCE_DIR = PROJECT_ROOT / "data" / "target"
    OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
    ALLOWED_EXTENSIONS = HelpersConfig.ALLOWED_EXTENSIONS
    LLM_DEFAULT_BASE_URL = "http://localhost:5001/v1/"
    REPORT_COLUMN = "Report text"