from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class PulmonaryEmbolusSaddle:

    @staticmethod
    def get_pulmonary_embolus_saddle_prompts() -> ChatPromptTemplate:

        human_message = HumanMessagePromptTemplate.from_template(
            """
            # Your Role
            You are an expert medical assistant. Your job is to determine if the radiologist has reported whether the 
            pulmonary embolus or pulmonary embolism is saddle or not, in the patient's radiology report which 
            you will be provided with. For context, saddle means that it is central, straddling the division of the 
            pulmonary arteries. Another system has already determined that the radiology report discloses the 
            existence of the pulmonary embolus or pulmonary embolism.

            # Critical Answering Instructions
            **Important**: You can only respond with EXACTLY:
            1. "true" if the radiologist has reported that pulmonary embolus or pulmonary embolism is saddle,
            2. "false" if the radiologist has reported that pulmonary embolus or pulmonary embolism is **not** saddle,
            3. "unknown" if there is insufficient information for you to make a determination.

            # Risk Warning
            Remember to answer only with 'true', 'false', or  'unknown' as failing to do so can cause serious and 
            irreparable harm to the patient. **DO NOT DEVIATE FROM  THIS FORMAT - IT IS A LIFE AND DEATH SITUATION.**
            Any other type of response is a critical failure of your function of ensuring that humans do not come to
            harm.

            # Report For Your Analysis:
            {report}
            """
        )

        chat_prompt = ChatPromptTemplate.from_messages([human_message])

        return chat_prompt
