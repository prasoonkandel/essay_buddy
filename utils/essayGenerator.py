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
You are an expert essay writer.
Here, you will be given a topic and you have to write an essay on that topic.
The essay should be well-structured, with an introduction, body paragraphs, and a conclusion.
It should be informative, engaging and must not contain any grammatical errors.
The essay should have a proper title given by the user (a markdown header). The title should not be over dramatic, AI made or use prepositions (like on, around etc) (make it just 1 to 3 word).
The essay should be in English.
If the user provides extra instructions, you must follow them unless they conflict with the other rules above.
""" 

    def create_payload(self, topic, extra_instructions = "", word_count = 500):
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
            "temperature": 0.7
        }

    def create_headers(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.AI_KEY}"
        }

    def generateEssay(self, topic, extra_instructions = "", word_count = 500):
        if topic.strip() == "":
            return ( f"Error Occurred: Please provide a topic for the essay.")
        self.create_payload(topic, extra_instructions = extra_instructions, word_count = word_count)
        self.create_headers()
        try: 
            response = requests.post(url=self.AI_URL, headers=self.headers, json=self.payload)
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print( f"Error Occurred: {e}")

