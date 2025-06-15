from langchain_core.language_models import BaseLanguageModel

from src.llm_manager.llm_config import LLMConfig
from src.llm_manager.llm_provider import LLMProvider
from src.llm_manager.ollama_gemma2_27b.ollama_gemma2_27b import OllamaGemma227b


class LLMFactory:

    @staticmethod
    def create_llm(config: LLMConfig):
        if config.provider == LLMProvider.GEMMA:
            return LLMFactory._create_gemma_llm(config)
        return None

    @staticmethod
    def _create_gemma_llm(config: LLMConfig) -> BaseLanguageModel:
        llm = OllamaGemma227b.get_llm(temperature=config.temperature,
                                      num_predict=config.max_tokens,
                                      num_gpu=config.gpu_layer_offload_count)
        return llm