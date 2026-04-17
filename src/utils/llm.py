import os
import json
from src.config import PRIMARY_MODEL, CHEAP_MODEL
from google import genai
from google.genai import types

class LLMInterface:
    def __init__(self):
        self.traces = []
        self.total_cost = 0.0
        self.total_tokens = 0
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        
        self.client = genai.Client(api_key=api_key)
        
    def call_llm(self, prompt: str, model_name: str = PRIMARY_MODEL, json_mode: bool = False) -> str:
        config = None
        if json_mode:
            config = types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        
        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config
        )
        
        # Tracking (GenAI v2 usage tracking)
        usage = response.usage_metadata
        tokens = usage.total_token_count if usage else 0
        cost = (tokens / 1000000) * 0.15 # Rough estimate for Flash 2.0
        
        self._add_trace(prompt, response.text, model_name, tokens, cost)
        return response.text

    def embed_text(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list:
        """Get embeddings using Gemini."""
        response = self.client.models.embed_content(
            model="text-embedding-004",
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type)
        )
        return response.embeddings[0].values

    def _add_trace(self, prompt, response, model, tokens, cost):
        self.traces.append({
            "prompt": prompt,
            "response": response,
            "model": model,
            "tokens": tokens,
            "cost": cost,
            "timestamp": str(os.path.getmtime(__file__)) # placeholder
        })
        self.total_tokens += tokens
        self.total_cost += cost

    def get_logs(self):
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "traces": self.traces
        }
