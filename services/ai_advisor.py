import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class ThreatAdvisor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            print("[Warning] GEMINI_API_KEY not found. Running in Mock Mode.")

    def generate_advice(self, threat_type: str, location: str, severity: str) -> str:
        """
        Takes threat details and asks AI for survival advice.
        """
        #  if no API key is provided (Mocking)
        if not self.client:
            return f"[Mock AI] Detected {threat_type} in {location}. Stay safe!"

        #  Prompt Engineering
        prompt = (
            f"You are an emergency survival assistant. "
            f"A {severity} threat '{threat_type}' has been reported in {location}. "
            f"Provide a short, actionable survival tip (max 2 sentences). "
            f"Do not use markdown formatting like bold or italics."
        )

        # real API call
        try:
            # model is to be changed
            response = self.client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                ),
            )
            return f"[AI Advisor] {response.text.strip()}"

        except Exception as e:
            return f"[AI Error] Could not generate advice: {e}"


