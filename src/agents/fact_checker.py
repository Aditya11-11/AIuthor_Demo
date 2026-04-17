from typing import Dict, Any, List
from src.agents.base import BaseAgent
from src.memory.schema import FactRecord

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
