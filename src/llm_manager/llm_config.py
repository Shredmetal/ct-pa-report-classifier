from dataclasses import dataclass
from typing import Optional, Union

from pydantic import SecretStr


@dataclass
class LLMConfig:
    provider: Optional[str] = None
    api_key: Optional[Union[str, SecretStr]] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    max_retries: Optional[int] = None
    timeout: Optional[float] = None
    gpu_layer_offload_count: Optional[int] = None
    base_url: Optional[str] = None