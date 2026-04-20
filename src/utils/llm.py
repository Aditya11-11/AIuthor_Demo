import os
from src.config import PRIMARY_MODEL
from google import genai
from google.genai import types
from datetime import datetime
import time
from google.genai import errors

class LLMInterface:
    def __init__(self):
        self.traces = []
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
        
        max_retries = 5
        retry_delay = 10
        
        for attempt in range(max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                
                try:
                    res_text = response.text
                except Exception as e:
                    print(f"[LLMInterface] Error accessing response text: {e}")
                    res_text = ""
                    
                if not res_text:
                    print(f"[LLMInterface] Received empty or blocked response from model.")
                    res_text = ""

                # Approximate token count (Gemini Flash prices: $0.075 / 1M in, $0.30 / 1M out)
                input_tokens = len(prompt) // 4
                output_tokens = len(res_text) // 4
                cost = (input_tokens * 0.000000075) + (output_tokens * 0.00000030)
                
                self._add_trace(prompt, res_text, model_name, input_tokens + output_tokens, cost)
                return res_text
                
            except errors.ClientError as e:
                if "429" in str(e) and attempt < max_retries:
                    wait = retry_delay * (2 ** attempt)
                    print(f"[LLMInterface] Rate limit hit (429). Retrying in {wait}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                else:
                    raise
            except Exception as e:
                if attempt < max_retries:
                    wait = retry_delay * (2 ** attempt)
                    print(f"[LLMInterface] Unexpected error: {e}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
        return ""

    def _add_trace(self, prompt, response, model, tokens, cost):
        self.traces.append({
            "prompt": prompt,
            "response": response,
            "model": model,
            "tokens": tokens,
            "cost": cost,
            "timestamp": str(datetime.now())
        })

    def get_logs(self):
        return {
            "traces": self.traces
        }
