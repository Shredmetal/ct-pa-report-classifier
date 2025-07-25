from dataclasses import dataclass

from src.api.routers.processor_router_config import ProcessorRouterConfig


@dataclass
class MiscRouterConfig:
    SOURCE_DIR = ProcessorRouterConfig.SOURCE_DIR
    OUTPUT_DIR = ProcessorRouterConfig.OUTPUT_DIR
    ALLOWED_DIRECTORIES = {
        "source": SOURCE_DIR,
        "output": OUTPUT_DIR
    }