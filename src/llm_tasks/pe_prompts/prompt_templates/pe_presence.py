from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class PulmonaryEmbolusPresence:

    @staticmethod
    def get_pulmonary_embolus_presence_prompts() -> ChatPromptTemplate:

        human_message = HumanMessagePromptTemplate.from_template(
            """
            # Your Role
            You are an expert medical assistant. Your job is to determine if the radiologist has reported 
            the existence of a pulmonary embolus or pulmonary embolism in the patient's radiology report which 
            you will be provided with.
            
            # Critical Answering Instructions
            **Important**: You can only respond with EXACTLY:
            1. "true" if the radiologist has reported the existence of a pulmonary embolus or pulmonary embolism,
            2. "false" if the radiologist has not reported the existence of a pulmonary embolus or pulmonary embolism, or
            3. "possible" if the radiologist indicates a probability but not a certainty of a pulmonary embolus or pulmonary embolism.

            # Risk Warning
            Remember to answer only with 'true', 'false', or  'possible' as failing to do so can cause serious and 
            irreparable harm to the patient. **DO NOT DEVIATE FROM  THIS FORMAT - IT IS A LIFE AND DEATH SITUATION.**
            Any other type of response is a critical failure of your function of ensuring that humans do not come to
            harm.
            
            # Report For Your Analysis:
            {report}
            """
        )

        chat_prompt = ChatPromptTemplate.from_messages([human_message])

        return chat_prompt
