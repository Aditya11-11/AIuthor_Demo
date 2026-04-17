from typing import Dict, Any
from src.agents.base import BaseAgent
from src.memory.schema import BookBrief, BookOutline, ChapterOutline
import json

class PlannerAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("Planner", model_name)

    def execute(self, brief: BookBrief, context: Dict[str, Any] = None) -> BookOutline:
        prompt = f"""
        You are the Lead Planner for AIuthor, an advanced agentic book writing system.
        Your task is to create a comprehensive outline for a publication-ready book based on the following brief:
        
        TOPIC: {brief.topic}
        READER PROFILE: {brief.reader_profile}
        LENGTH: {brief.length}
        TONALITY: {brief.tonality}
        GENRE: {brief.genre}
        
        The book MUST include:
        1. Front Matter: half-title, title, copyright (ISBN placeholder, edition, rights, CIP block), dedication, epigraph, TOC, foreword, preface, acknowledgments, introduction.
        2. Body: Chapters with consistent structure.
        3. Back Matter: afterword, appendix, glossary, references, about-the-author, back-cover copy.
        
        Output your plan in a structured JSON format following this schema:
        {{
            "title": "Book Title",
            "front_matter_plan": ["list", "of", "elements"],
            "chapters": [
                {{
                    "chapter_number": 1,
                    "title": "Chapter Title",
                    "summary": "Contextual summary of the chapter",
                    "key_points": ["point 1", "point 2"],
                    "estimated_word_count": 2500
                }}
            ],
            "back_matter_plan": ["list", "of", "elements"]
        }}
        """
        
        # In a real implementation, this would call the LLM.
        # For the sake of this project, I will implement the orchestration logic.
        # I'll create a mock LLM call for now or use a tool if available.
        
        print(f"[{self.name}] Planning book: {brief.topic}")
        return prompt
