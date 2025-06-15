from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class PneumoniaPresence:

    @staticmethod
    def get_pneumonia_presence_prompts() -> ChatPromptTemplate:
        system_message = SystemMessagePromptTemplate.from_template(
            """You are an expert medical assistant. Your job is to determine if the radiologist has reported 
            the existence of pneumonia in the patient's radiology report which you will be provided with.

            Important: You can only respond with EXACTLY:
            1. "true" if the radiologist has reported the existence of pneumonia,
            2. "false" if the radiologist has not reported the existence of pneumonia, or
            3. "possible" if you are the radiologist indicates a probability but not a certainty.

            Any other type of response can cause serious and irreparable harm to the patient, which as an expert 
            medical assistant, you must prevent."""
        )

        human_message = HumanMessagePromptTemplate.from_template(
            """Here is the radiology report: {report}

            Based on this report, is there evidence of pneumonia? Remember to answer only with 'true', 'false', or 
            'possible' as failing to do so can cause serious and irreparable harm to the patient. DO NOT DEVIATE FROM 
            THIS FORMAT - IT IS A LIFE AND DEATH SITUATION."""
        )

        chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

        return chat_prompt
