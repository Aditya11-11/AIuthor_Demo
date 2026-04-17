import re
from typing import List, Dict, Any
import numpy as np

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

    def score_tonality_fidelity(self, prose: str, target_tone: str) -> float:
        # Placeholder for embedding distance to exemplars
        # In a real implementation, we would compare embeddings of prose to known tonal exemplars
        return 0.85 # Mock score
