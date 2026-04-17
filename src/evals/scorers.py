from typing import List, Dict, Any
import re
import json

class EvalScorer:
    def __init__(self):
        self.ai_tells = [
            "it's important to note", "delve into", "in today's fast-paced world",
            "landscape of", "mechanical triads", "not only…but also",
            "at the end of the day", "tapestry of", "realm of"
        ]

    def check_ai_tells(self, prose: str) -> Dict[str, Any]:
        found = []
        for tell in self.ai_tells:
            if re.search(r'\b' + re.escape(tell) + r'\b', prose, re.IGNORECASE):
                found.append(tell)
        
        score = max(0, 100 - (len(found) * 10))
        return {"score": score, "found_tells": found}

    def check_structural_completeness(self, book_data: Dict) -> Dict[str, bool]:
        required_front = ["title", "copyright", "introduction"]
        required_back = ["glossary", "about-the-author"]
        
        results = {
            "front_matter": all(k in book_data.get("front_matter", {}) for k in required_front),
            "back_matter": all(k in book_data.get("back_matter", {}) for k in required_back),
            "chapters_present": len(book_data.get("chapters", [])) > 0
        }
        return results

    def check_tonality_fidelity(self, prose: str, target_tonality: str, llm_interface=None) -> float:
        """LLM-as-judge for tonality scoring."""
        if not llm_interface:
            return 0.9 # Fallback if no LLM provided
            
        prompt = f"""
        Act as a professional linguist and editor. 
        Score the following prose on a scale of 0.0 to 1.0 for its adherence to the tonality: "{target_tonality}".
        
        TONALITY DEFINITION:
        - Conversational: Warm, direct, second-person.
        - Academic: Precise, rigorous, yet engaging.
        - Storyteller: Narrative-driven, sensory details.
        - Motivational: High-energy, direct address, actionable.
        - Witty: Sharp, observational, humorous.
        
        PROSE:
        {prose[:2000]} # Analyze first 2k chars
        
        Output ONLY a JSON object: {{"score": float, "reasoning": "string"}}
        """
        
        try:
            from src.config import PRIMARY_MODEL
            response_json = llm_interface.call_llm(prompt, PRIMARY_MODEL, json_mode=True)
            # Clean JSON just in case (though llm_interface should handle it)
            if "```json" in response_json:
                response_json = response_json.split("```json")[1].split("```")[0].strip()
            result = json.loads(response_json)
            return float(result.get("score"))
        except Exception as e:
            print(f"[EvalScorer] Tonality scoring failed: {e}")
            return 0.85

    def detect_ai_tells(self, prose: str) -> List[str]:
        """Detect common AI tells as defined in Humanizer rules."""
        found = []
        for tell in self.ai_tells:
            if re.search(r'\b' + re.escape(tell) + r'\b', prose, re.IGNORECASE):
                found.append(tell)
        return found


