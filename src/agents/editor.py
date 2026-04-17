from typing import Dict, Any
from src.agents.base import BaseAgent

class EditorAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("Editor", model_name)

    def execute(self, prose: str, chapter_number: int, context: Dict[str, Any] = None) -> str:
        prompt = f"""
        You are the Lead Editor for AIuthor.
        Review Chapter {chapter_number} for flow, consistency, and structural integrity.
        
        STRICTURES:
        1. Ensure smooth transitions between paragraphs.
        2. Check for tonal consistency with previous chapters.
        3. Identify and fix any repetition or clunky phrasing.
        4. Do NOT rewrite the entire chapter, just polish it.
        
        PROSE:
        {prose}
        
        Output the polished prose.
        """
        
        print(f"[{self.name}] Editing chapter {chapter_number}")
        return prompt
