from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class LungBronchiectasis:

    @staticmethod
    def get_lung_bronchiectasis_prompts() -> ChatPromptTemplate:
        human_message = HumanMessagePromptTemplate.from_template(
            """
            # Your Role
            You are an expert medical assistant. Your job is to determine if the radiologist has reported lung 
            emphysema in the patient's radiology report which you will be provided with. Another system has already 
            determined that the radiology report discloses the existence of a lung abnormality. Emphysema is 
            degradation of the walls of the spongy parts of the lungs, leading to larger air spaces with less surface 
            area.

            # Critical Answering Instructions
            **Important**: You can only respond with EXACTLY:
            1. "true" if the radiologist has reported a lung emphysema,
            2. "false" if the radiologist has not reported a lung emphysema, or
            3. "possible" if the radiology report indicates a probability but not a certainty of a lung emphysema.

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
