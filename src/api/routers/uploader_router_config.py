from dataclasses import dataclass

from src.api.helpers.helpers_config import HelpersConfig
from src.api.routers.processor_router_config import ProcessorRouterConfig


@dataclass
class UploaderRouterConfig:
    UPLOAD_DIR = ProcessorRouterConfig.SOURCE_DIR
    MAX_FILE_SIZE = 50 * 1024 * 1024
    ALLOWED_EXTENSIONS = HelpersConfig.ALLOWED_EXTENSIONS