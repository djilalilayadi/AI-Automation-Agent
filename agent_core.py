import os
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class AICore:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.memory = []  # For storing past interactions
        
    def understand_task(self, user_input: str) -> Dict:
        """Use LLM to interpret the user's request"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a task interpreter for an automation AI. Identify the action, target, and output format."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        
        interpretation = response.choices[0].message.content
        self.memory.append({"input": user_input, "interpretation": interpretation})
        return self._parse_interpretation(interpretation)
    
    def _parse_interpretation(self, text: str) -> Dict:
        """Convert LLM output into structured data"""
        # This is simplified - you'd want more robust parsing
        return {
            "action": "scrape" if "scrape" in text.lower() else "unknown",
            "target": text.split("from ")[-1].split(" to")[0] if "from" in text else "",
            "output": "spreadsheet" if "spreadsheet" in text.lower() else "unknown"
        }