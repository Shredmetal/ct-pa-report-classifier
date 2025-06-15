from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI

from src.llm_manager.llm_config import LLMConfig


class LLMFactory:

    @staticmethod
    def create_llm(config: LLMConfig):
        if config.provider is None:
            return LLMFactory._create_oai_api_llm(config)
        return None

    @staticmethod
    def _create_oai_api_llm(config: LLMConfig) -> BaseLanguageModel:
        llm = ChatOpenAI(
            base_url=config.base_url,
            temperature=config.temperature,
            api_key="unused",
            model="medgemma:27b:q4"
        )
        return llm