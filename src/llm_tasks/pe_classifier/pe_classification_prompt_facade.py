from src.llm_tasks.pe_classifier.pe_heart_strain import PulmonaryEmbolusHeartStrain
from src.llm_tasks.pe_classifier.pe_large import PulmonaryEmbolusLarge
from src.llm_tasks.pe_classifier.pe_laterality import PulmonaryEmbolusLaterality
from src.llm_tasks.pe_classifier.pe_presence import PulmonaryEmbolusPresence
from src.llm_tasks.pe_classifier.pe_saddle import PulmonaryEmbolusSaddle


class PeClassificationPromptFacade:

    def __init__(self):
        self.presence_prompt = PulmonaryEmbolusPresence().get_pulmonary_embolus_presence_prompts()
        self.size_prompt = PulmonaryEmbolusLarge.get_pulmonary_embolus_large_prompts()
        self.saddle_prompt = PulmonaryEmbolusSaddle().get_pulmonary_embolus_saddle_prompts()
        self.laterality_prompt = PulmonaryEmbolusLaterality().get_pulmonary_embolus_laterality_prompts()
        self.heart_strain = PulmonaryEmbolusHeartStrain().get_pulmonary_embolus_heart_strain_prompts()
