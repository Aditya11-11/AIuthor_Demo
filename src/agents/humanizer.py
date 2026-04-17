from typing import Dict, Any
from src.agents.base import BaseAgent

class HumanizerAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("Humanizer", model_name)

    def execute(self, prose: str, tonality: str, context: Dict[str, Any] = None) -> str:
        prompt = f"""
        You are the Humanizer for AIuthor.
        Your task is to refine the following prose to make it sound more human and less like AI.
        
        TONALITY: {tonality}
        
        STRICT RULES:
        1. Eliminate AI tells: "it's important to note," "delve into," "in today's fast-paced world," "landscape of," mechanical triads, symmetric "not only…but also".
        2. Vary sentence rhythm (short vs. long).
        3. Use domain-drawn metaphors.
        4. Ensure a conversational hook where appropriate.
        5. If tonality is "{tonality}", ensure specific presets are applied:
           - Conversational: Warm, direct, second-person.
           - Academic: Precise, rigorous, yet engaging.
           - Storyteller: Narrative-driven, sensory details.
           - Motivational: High-energy, direct address, actionable.
           - Witty: Sharp, observational, humorous.
        
        PROSE TO REWRITE:
        {prose}
        
        Output only the refined humanized prose.
        """
        
        print(f"[{self.name}] Humanizing prose for tonality: {tonality}")
        return prompt
        
    def get_prompt_dossier_rules(self) -> str:
        return "Rules for Humanizer: Eliminate AI tells, vary sentence rhythm, use domain-drawn metaphors, etc."
