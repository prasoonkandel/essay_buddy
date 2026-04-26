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
Here, you will be given a query and you have to write an essay on that topic.
The essay should be well-structured, with an introduction, body paragraphs, and a conclusion.
It should be informative, engaging and must not contain any grammatical errors.
The essay should have a proper title given by the user. The title should not be over dramatic or AI made (make it just 1 to 3 words). The essay should be around 500 words. The essay should be in English.
"""

    

    def create_payload(self, query):
        systemInstructions = self.getSystemInstructions()
        self.payload = {
            "model": self.MODEL,
            "messages": [
                {"role": "system", "content": systemInstructions},
                {"role": "user", "content": query}
            ],
            "temperature": 0.7
        }

    def create_headers(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.AI_KEY}"
        }

