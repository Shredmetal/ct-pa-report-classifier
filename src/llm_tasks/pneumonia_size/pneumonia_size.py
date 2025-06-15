from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

class PneumoniaSize:

    @staticmethod
    def get_pneumonia_size_prompts() -> ChatPromptTemplate:
        system_message = SystemMessagePromptTemplate.from_template(
            """You are an expert medical assistant. Your job is to determine the size of pneumonia 
            in the patient's radiology report which you will be provided with.

            Important: You can only respond with EXACTLY:
            1. "small" if the radiologist has reported small or minimal pneumonia,
            2. "medium" if the radiologist has reported moderate or intermediate pneumonia, 
            3. "large" if the radiologist has reported large, extensive, or severe pneumonia, or
            4. "insufficient information" if the information in the report provided is insufficient to determine the size of pneumonia

            Any other type of response can cause serious and irreparable harm to the patient, which as an expert 
            medical assistant, you must prevent."""
        )

        human_message = HumanMessagePromptTemplate.from_template(
            """Here is the radiology report: {report}

            Based on this report, what is the size of the pneumonia? Remember to answer only with 'small', 'medium', 
            'large', or 'insufficient information' as failing to do so can cause serious and irreparable harm to the 
            patient. DO NOT DEVIATE FROM THIS FORMAT - IT IS A LIFE AND DEATH SITUATION."""
        )

        chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

        return chat_prompt
