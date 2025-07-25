from src.llm_tasks.lung_abnormality_prompts.prompt_templates.lung_abnormality import LungAbnormality
from src.llm_tasks.lung_abnormality_prompts.prompt_templates.lung_bronchiectasis import LungBronchiectasis
from src.llm_tasks.lung_abnormality_prompts.prompt_templates.lung_bullae import LungBullae
from src.llm_tasks.lung_abnormality_prompts.prompt_templates.lung_emphysema import LungEmphysema


class LungAbnormalityPromptFacade:

    def __init__(self):
        self.lung_abnormality_prompt = LungAbnormality().get_lung_abnormality_prompts()
        self.lung_bronchiectasis_prompt = LungBronchiectasis().get_lung_bronchiectasis_prompts()
        self.lung_emphysema_prompt = LungEmphysema().get_lung_emphysema_prompts()
        self.lung_bullae_prompt = LungBullae().get_lung_bullae_prompts()