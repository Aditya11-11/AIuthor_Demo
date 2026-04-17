from typing import Dict, Any, List
from src.agents.base import BaseAgent
from src.memory.schema import BookBrief, BookOutline

class FrontMatterAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("FrontMatter", model_name)

    def execute(self, brief: BookBrief, outline: BookOutline) -> str:
        prompt = f"""
        You are the Front Matter Specialist for AIuthor.
        Generate the front matter for the book: {outline.title}.
        
        TONALITY: {brief.tonality}
        READER PROFILE: {brief.reader_profile}
        
        REQUIRED ELEMENTS:
        - half-title
        - title page
        - copyright (ISBN 978-0-0000000-0-0, Edition 1.0, Rights: All Rights Reserved, CIP Block included)
        - dedication
        - epigraph
        - foreword
        - preface
        - acknowledgments
        - introduction
        
        STRICTURES:
        - Match {brief.tonality} tone in ALL elements.
        - Humanize the prose. Eliminate AI tells.
        - Layout the Copyright page as a formal CIP block.
        
        Output only a JSON dictionary with these keys.
        """
        return prompt
