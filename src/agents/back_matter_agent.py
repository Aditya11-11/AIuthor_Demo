from typing import Dict, Any, List
from src.agents.base import BaseAgent
from src.memory.schema import BookBrief, BookOutline, MemoryState

class BackMatterAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("BackMatter", model_name)

    def execute(self, brief: BookBrief, outline: BookOutline, memory: MemoryState) -> str:
        # Extract glossary terms from memory
        terms = [f.fact for f in memory.fact_registry[:15]]
        
        prompt = f"""
        You are the Back Matter Specialist for AIuthor.
        Generate the back matter for the book: {outline.title}.
        
        TONALITY: {brief.tonality}
        
        REQUIRED ELEMENTS:
        - afterword
        - appendix
        - glossary (based on these terms: {', '.join(terms)})
        - references (based on Fact Registry)
        - about-the-author
        - back-cover copy
        
        STRICTURES:
        - Match {brief.tonality} tone.
        - Prose must be humanized.
        
        Output only a JSON dictionary with these keys.
        """
        return prompt
