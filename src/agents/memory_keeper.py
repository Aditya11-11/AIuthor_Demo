from typing import Dict, Any, List
from src.agents.base import BaseAgent
from src.memory.schema import MemoryState, FactRecord, CharacterRecord, Callback

class MemoryKeeperAgent(BaseAgent):
    def __init__(self, model_name: str):
        super().__init__("MemoryKeeper", model_name)

    def execute(self, chapter_content: str, current_memory: MemoryState, chapter_number: int) -> MemoryState:
        prompt = f"""
        You are the Memory Keeper for AIuthor.
        Analyze the following chapter content and update the memory state.
        
        CHAPTER {chapter_number} CONTENT:
        {chapter_content}
        
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
