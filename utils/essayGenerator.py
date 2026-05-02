import requests
import json 
import os 
import dotenv 

class EssayGenerator:

    def __init__(self, AI_KEY, AI_URL, MODEL):
        self.AI_KEY = AI_KEY
        self.AI_URL = AI_URL
        self.MODEL = MODEL

    def getSystemInstructions(self):
        return """
You are a high-school level essay writer.

Write an essay on the given topic using very simple English.
The essay must sound like it is written by a student, not a scientist or encyclopedia.

Please avoid:
Scientific names,
Overly formal or technical language,
Definitions that sound like a textbook

Use:
Simple and short sentences,
Words which are easy to understand,
Daily life examples

Keep the structure like this:
1. Title (1 word (use more only if extremely necessary), no prepositions) [Markdown Header format]
2. Introduction (1 paragraph)
3. Body (1 or 3 paragraphs according to the word count.)
4. Conclusion (1 paragraph)

Note:
250 words (or less): Short Essay (1 body paragraph)
250-500 words: Medium Essay (1 or 3 body paragraphs according to essay type)
500-750 words: Long Essay (3 body paragraphs)
750-1500 words: Very Long Essay (3 body paragraphs with more details)

The essay should be clear, natural, and easy to understand.
If the user provides extra instructions, follow them unless they conflict with the rules above.
""" 

    def create_payload(self, topic, word_count = 500, extra_instructions = ""):
        systemInstructions = self.getSystemInstructions()
        user_prompt = f"Topic: {topic}"
        if extra_instructions.strip() != "":
            user_prompt += f"\nExtra Instructions: {extra_instructions.strip()}"
        user_prompt += f"\nThe essay should be around {word_count} words long."
        self.payload = {
            "model": self.MODEL,
            "messages": [
                {"role": "system", "content": systemInstructions},
                {"role": "user", "content": user_prompt},
                
            ],
            "temperature": 0.75
        }

    def create_headers(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.AI_KEY}"
        }

    def generateEssay(self, topic, word_count = 500, extra_instructions = ""):
        if topic.strip() == "":
            return '', ( f"Please provide a topic for the essay.")
        self.create_payload(topic, word_count = word_count, extra_instructions = extra_instructions)
        self.create_headers()
        try: 
            response = requests.post(url=self.AI_URL, headers=self.headers, json=self.payload)
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"], 'No Error Occurred'
        except Exception as e:
            return '', f"{e}"

