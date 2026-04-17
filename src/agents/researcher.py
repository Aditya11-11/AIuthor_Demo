from typing import Dict, Any, List
from src.agents.base import BaseAgent
from src.memory.schema import ChapterOutline, FactRecord

class ResearcherAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("Researcher", model_name)

    def execute(self, chapter: ChapterOutline, context: Dict[str, Any] = None) -> List[FactRecord]:
        prompt = f"""
        You are the Lead Researcher for AIuthor.
        Your task is to gather grounded facts and research for the following chapter:
        
        CHAPTER {chapter.chapter_number}: {chapter.title}
        SUMMARY: {chapter.summary}
        KEY POINTS: {', '.join(chapter.key_points)}
        
        Focus on accuracy and depth. Avoid generic information. Use domain-specific metaphors and varied factual data.
        
        Output a list of facts with sources (if applicable) and confidence scores.
        Format: JSON list of FactRecord objects.
        """
        
        print(f"[{self.name}] Researching chapter {chapter.chapter_number}: {chapter.title}")
        return prompt
