from typing import Dict, Any, List
from src.agents.base import BaseAgent
from src.memory.schema import ChapterOutline, FactRecord, MemoryState

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
