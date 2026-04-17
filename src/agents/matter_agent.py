from typing import Dict, Any, List
from src.memory.schema import BookBrief, BookOutline, MemoryState

class MatterAgent:
    def __init__(self, model_name: str):
        self.name = "MatterGenerator"
        self.model_name = model_name

    def generate_front_matter(self, brief: BookBrief, outline: BookOutline) -> Dict[str, str]:
        prompt = f"""
        You are the Front Matter Specialist for AIuthor.
        Generate the front matter for the book: {outline.title}.
        
        TONALITY: {brief.tonality}
        READER PROFILE: {brief.reader_profile}
        
        REQUIRED ELEMENTS:
        - Half-title
        - Title Page (Title, Subtitle, Author Name)
        - Copyright Page (Include ISBN placeholder, Edition, Rights, CIP block)
        - Dedication
        - Epigraph
        - Foreword
        - Preface
        - Acknowledgments
        - Introduction
        
        STRICTURES:
        - Match the book's tonality ({brief.tonality}) in ALL elements (even the copyright block should have a slight tonal tint if appropriate, but keeping legalistic structure).
        - Humanize the prose. No AI tells.
        
        Output a JSON dictionary where keys are element names and values are the content.
        """
        print(f"[{self.name}] Generating Front Matter for: {outline.title}")
        return prompt

    def generate_back_matter(self, brief: BookBrief, outline: BookOutline, memory: MemoryState) -> Dict[str, str]:
        glossary_terms = ", ".join([f.fact for f in memory.fact_registry[:10]]) # Simple selection
        prompt = f"""
        You are the Back Matter Specialist for AIuthor.
        Generate the back matter for the book: {outline.title}.
        
        TONALITY: {brief.tonality}
        
        REQUIRED ELEMENTS:
        - Afterword
        - Appendix
        - Glossary (Define these terms based on the book: {glossary_terms})
        - References (Real-sounding but clearly marked if synthetic, based on facts)
        - About the Author
        - Back-cover copy
        
        STRICTURES:
        - Match the book's tonality ({brief.tonality}).
        - Humanize the prose.
        
        Output a JSON dictionary where keys are element names and values are the content.
        """
        print(f"[{self.name}] Generating Back Matter for: {outline.title}")
        return prompt
