from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class PulmonaryEmbolusLaterality:

    @staticmethod
    def get_pulmonary_embolus_laterality_prompts() -> ChatPromptTemplate:
        human_message = HumanMessagePromptTemplate.from_template(
            """
            # Your Role
            You are an expert medical assistant. Your job is to determine the side on which the radiologist has reported 
            whether the existence of a pulmonary embolus or pulmonary embolism in the patient's radiology report which 
            you will be provided with. Another system has already determined that the radiology report discloses the 
            existence of the pulmonary embolus or pulmonary embolism, and that the pulmonary embolus or pulmonary 
            embolism is not saddle (i.e. central, straddling the division of the pulmonary arteries).

            # Critical Answering Instructions
            **Important**: You can only respond with EXACTLY:
            1. "right" if the radiologist has reported that pulmonary embolus or pulmonary embolism is on the right,
            2. "left" if the radiologist has reported that pulmonary embolus or pulmonary embolism is on the left,
            3. "unknown" if there is insufficient information for you to make a determination.

            # Risk Warning
            Remember to answer only with 'right', 'left', or  'unknown' as failing to do so can cause serious and 
            irreparable harm to the patient. **DO NOT DEVIATE FROM  THIS FORMAT - IT IS A LIFE AND DEATH SITUATION.**
            Any other type of response is a critical failure of your function of ensuring that humans do not come to
            harm.

            # Report For Your Analysis:
            {report}
            """
        )

        chat_prompt = ChatPromptTemplate.from_messages([human_message])

        return chat_prompt
