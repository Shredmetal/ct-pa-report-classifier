import string

from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any

from src.llm_tasks.pe_prompts.pe_classification_prompt_facade import PeClassificationPromptFacade

class RadiologyReportStructuredDataExtractor:

    def __init__(self, llm):
        self.llm = llm
        self.prompt_facade = PeClassificationPromptFacade()
        self.output_parser = StrOutputParser()

    def extract_pe_data(self, report: str) -> Dict[str, Any]:
        presence_chain = self.prompt_facade.presence_prompt | self.llm | self.output_parser
        largeness_chain = self.prompt_facade.size_prompt | self.llm | self.output_parser
        saddle_chain = self.prompt_facade.saddle_prompt | self.llm | self.output_parser
        laterality_chain = self.prompt_facade.laterality_prompt | self.llm | self.output_parser
        heart_strain_chain = self.prompt_facade.heart_strain | self.llm | self.output_parser

        presence_result = self._clean_output(presence_chain.invoke({"report": report}))
        heart_strain_result = self._clean_output(heart_strain_chain.invoke({"report": report}))

        if presence_result == "false":

            largeness_result = "not applicable"
            saddle_result = "not applicable"
            laterality_result = "not applicable"
        else:

            largeness_result = self._clean_output(largeness_chain.invoke({"report": report}))
            saddle_result = self._clean_output(saddle_chain.invoke({"report": report}))

            if saddle_result == "false" or saddle_result == "unknown":
                laterality_result = self._clean_output(laterality_chain.invoke({"report": report}))
            else:
                laterality_result = "not applicable"

        return {
            "report": report,
            "pe_presence": presence_result,
            "pe_large": largeness_result,
            "pe_saddle": saddle_result,
            "pe_laterality": laterality_result,
            "heart_strain": heart_strain_result
        }

    @staticmethod
    def _clean_output(llm_output: str) -> str:
        return llm_output.strip(string.whitespace + '\'"').lower()
