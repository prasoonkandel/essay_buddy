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
1. Title (1 to 3 simple words, no prepositions)
2. Introduction
3. Body (3 to 5 paragraphs according to the word count)
4. Conclusion

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

