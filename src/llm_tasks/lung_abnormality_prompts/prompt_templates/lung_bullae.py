from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class LungBullae:

    @staticmethod
    def get_lung_bullae_prompts() -> ChatPromptTemplate:
        human_message = HumanMessagePromptTemplate.from_template(
            """
            # Your Role
            You are an expert medical assistant. Your job is to determine if the radiologist has reported lung 
            bullae in the patient's radiology report which you will be provided with. Another system has already 
            determined that the radiology report discloses the existence of a lung abnormality. Bullae is 
            type of emphysema with large (>10mm) ‘bubbles’ with minimal surfaces for gas exchange. More flexible than 
            regular lung - expands more on breathing in, reducing effectiveness of healthy lung.

            # Critical Answering Instructions
            **Important**: You can only respond with EXACTLY:
            1. "true" if the radiologist has reported a lung bullae,
            2. "false" if the radiologist has not reported a lung bullae, or
            3. "possible" if the radiology report indicates a probability but not a certainty of a lung bullae.

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
