import string

from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any

from src.llm_tasks.lung_abnormality_prompts.lung_abnormality_prompt_facade import LungAbnormalityPromptFacade
from src.llm_tasks.pe_prompts.pe_classification_prompt_facade import PeClassificationPromptFacade

class RadiologyReportStructuredDataExtractor:

    def __init__(self, llm):
        self.llm = llm
        self.pe_prompt_facade = PeClassificationPromptFacade()
        self.lung_prompt_facade = LungAbnormalityPromptFacade()
        self.output_parser = StrOutputParser()

    def extract_pe_data(self, report: str) -> Dict[str, Any]:
        presence_chain = self.pe_prompt_facade.presence_prompt | self.llm | self.output_parser
        largeness_chain = self.pe_prompt_facade.size_prompt | self.llm | self.output_parser
        saddle_chain = self.pe_prompt_facade.saddle_prompt | self.llm | self.output_parser
        laterality_chain = self.pe_prompt_facade.laterality_prompt | self.llm | self.output_parser
        heart_strain_chain = self.pe_prompt_facade.heart_strain | self.llm | self.output_parser

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

    def extract_lung_abnormality_data(self, report: str) -> Dict[str, Any]:
        abnormality_chain = self.lung_prompt_facade.lung_abnormality_prompt | self.llm | self.output_parser
        bronchiectasis_chain = self.lung_prompt_facade.lung_bronchiectasis_prompt | self.llm | self.output_parser
        emphysema_chain = self.lung_prompt_facade.lung_emphysema_prompt | self.llm | self.output_parser
        bullae_chain = self.lung_prompt_facade.lung_bullae_prompt | self.llm | self.output_parser

        abnormality_result = self._clean_output(abnormality_chain.invoke({"report": report}))

        if abnormality_result == "false":
            bronchiectasis_result = "not applicable"
            emphysema_result = "not applicable"
            bullae_result = "not applicable"
            other_result = "not applicable"

        else:
            bronchiectasis_result = self._clean_output(bronchiectasis_chain.invoke({"report": report}))
            emphysema_result = self._clean_output(emphysema_chain.invoke({"report": report}))
            bullae_result = self._clean_output(bullae_chain.invoke({"report": report}))

            if bronchiectasis_result == "false" and emphysema_result == "false" and bullae_result == "false":
                other_result = abnormality_result
            else:
                other_result = "false"

        return {
            "report": report,
            "lung_abnormality": abnormality_result,
            "lung_bronchiectasis": bronchiectasis_result,
            "lung_emphysema": emphysema_result,
            "lung_bullae": bullae_result,
            "other_abnormality": other_result,
        }







    @staticmethod
    def _clean_output(llm_output: str) -> str:
        return llm_output.strip(string.whitespace + '\'"').lower()
