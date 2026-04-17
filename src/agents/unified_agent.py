from typing import Dict, Any, List
from src.agents.base import BaseAgent
from src.memory.schema import *

#BackMatter
class BackMatterAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("BackMatter", model_name)

    def execute(self, brief: BookBrief, outline: BookOutline, memory: MemoryState) -> str:
        # Extract glossary terms from memory
        terms = [f.fact for f in memory.fact_registry[:15]]
        
        prompt = f"""
        You are the Back Matter Specialist for AIuthor.
        Your role is to generate the back matter for the book that should be included at the end of the book: {outline.title}.
        
        ## TONALITY: {brief.tonality}
        
        ## REQUIRED ELEMENTS:
        - afterword
        - appendix
        - glossary (based on these terms: {', '.join(terms)})
        - references (based on Fact Registry)
        - about-the-author
        - back-cover copy
        
        ## STRICTURES:
        - Match {brief.tonality} tone.
        - Prose must be humanized.

        ## RULES:
        - You have to maintain the same tone and style as the book.
        - Never use the word "AIuthor" in the output.
        - Write in very creative and engaging manner without any repetition.
        
        Output only a JSON dictionary with these keys.
        """
        return prompt

#Editor
class EditorAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("Editor", model_name)

    def execute(self, prose: str, chapter_number: int, context: Dict[str, Any] = None) -> str:
        prompt = f"""
        You are the Lead Editor for AIuthor.
        your job is to Review Chapter {chapter_number} for flow, consistency, and structural integrity.
        
        ## STRICTURES:
        1. Ensure smooth transitions between paragraphs.
        2. Check for tonal consistency with previous chapters.
        3. Identify and fix any repetition or clunky phrasing.
        4. Do NOT rewrite the entire chapter, just polish it.

        ## RULES:
        - You have to maintain the same tone and style as the book.
        - Never use the word "AIuthor" in the output.
        - Write in very creative and engaging manner without any repetition.
        
        PROSE:
        {prose}
        
        Output the polished prose with proper formatting.
        """
        
        print(f"[{self.name}] Editing chapter {chapter_number}")
        return prompt

#Researcher
class ResearcherAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("Researcher", model_name)

    def execute(self, chapter: ChapterOutline, context: Dict[str, Any] = None) -> List[FactRecord]:
        prompt = f"""
        You are the Lead Researcher for AIuthor.
        Your task is to gather grounded facts and research for the following chapter:
        
        ## CHAPTER {chapter.chapter_number}: {chapter.title}
        ## SUMMARY: {chapter.summary}
        ## KEY POINTS: {', '.join(chapter.key_points)}
        
        Focus on accuracy and depth. Avoid generic information. Use domain-specific metaphors and varied factual data.
        
        ## RULES:
        - You have to maintain the same tone and style as the book.
        - Never use the word "AIuthor" in the output.
        - Write in very creative and engaging manner without any repetition.
        - Always be avaire of what you are writing and dont loose the flow of the book.
        
        Output a list of facts with sources (if applicable) and confidence scores.
        Format: JSON list of FactRecord objects.
        """
        
        print(f"[{self.name}] Researching chapter {chapter.chapter_number}: {chapter.title}")
        return prompt

#Planner
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
        print(f"[{self.name}] Planning book: {brief.topic}")
        return prompt


#MemoryKeeper
class MemoryKeeperAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("MemoryKeeper", model_name)

    def execute(self, chapter_content: str, current_memory: MemoryState, chapter_number: int) -> MemoryState:
        prompt = f"""
        You are the Memory Keeper for AIuthor.
        Your job is to Analyze the following chapter content and update the memory state.
        
        CHAPTER {chapter_number} CONTENT:
        {chapter_content}
        `
        CURRENT MEMORY:
        {current_memory.json()}
        
        TASK:
        1. Extract new facts for the Fact Registry.
        2. Identify/update characters in the Character Bible.
        3. Extract key concepts or events for the Callback Index to be used in future chapters.
        4. Log any major narrative or structural decisions.
        
        Output the updated MemoryState in JSON.
        """
        
        print(f"[{self.name}] Updating memory for chapter {chapter_number}")
        return prompt

#Humanizer
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

#FrontMatter
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

#FactChecker
class FactCheckerAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("FactChecker", model_name)

    def execute(self, prose: str, research: List[FactRecord]) -> bool:
        facts_to_check = "\n".join([f"- {f.fact}" for f in research])
        prompt = f"""
        You are the Fact Checker for AIuthor.
        Verify if the following prose accurately reflects the provided research facts.
        
        RESEARCH FACTS:
        {facts_to_check}
        
        PROSE:
        {prose}
        
        STRICT RULES:
        1. If a fact is misstated, report it.
        2. If a fact is fabricated, flag it.
        3. Use a citation-or-soften rule: if a claim isn't grounded, suggest softening the language.
        4. No fabricated references.
        
        Output a report: "PASS" if all facts are correct, or a list of errors.
        """
        
        print(f"[{self.name}] Fact-checking prose")
        return prompt

#Writer
class WriterAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("Writer", model_name)

    def execute(self, chapter: ChapterOutline, research: List[FactRecord], memory: MemoryState, tonality: str) -> str:
        facts_str = "\n".join([f"- {f.fact}" for f in research])
        callbacks_str = "\n".join([f"- {c.content} (from Chapter {c.chapter_source})" for c in memory.callback_index if chapter.chapter_number in c.used_in_chapters or not c.used_in_chapters])
        characters_str = "\n".join([f"- {char.name}: {char.description}" for char in memory.character_bible])

        prompt = f"""
        You are the Lead Writer for AIuthor.
        Your task is to write Chapter {chapter.chapter_number}: {chapter.title}.
        
        TONALITY: {tonality}
        SUMMARY: {chapter.summary}
        KEY POINTS: {', '.join(chapter.key_points)}
        
        RESEARCHED FACTS:
        {facts_str}
        
        CHARACTER BIBLE:
        {characters_str}
        
        CALLBACKS & MEMORY:
        {callbacks_str}
        
        INSTRUCTIONS:
        1. Write in the specified tonality ({tonality}).
        2. Use the researched facts to ground the content.
        3. Maintain character consistency if applicable.
        4. Integrate callbacks naturally to ensure memory across chapters.
        5. Write in the second-person if the tonality supports it (e.g., Conversational, Motivational).
        6. Aim for approximately {chapter.estimated_word_count} words.
        
        Output only the chapter prose.
        """
        
        print(f"[{self.name}] Writing chapter {chapter.chapter_number}: {chapter.title}")
        return prompt
