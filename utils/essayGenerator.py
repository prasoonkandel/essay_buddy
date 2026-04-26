import requests 
import json 
import os 
import dotenv 

class EssayGenerator:

    def __init__(self, AI_KEY, AI_URL, MODEL):
        self.AI_KEY = AI_KEY
        self.AI_URL = AI_URL
        self.MODEL = MODEL

    def create_payload(self, query):
        system_instruction = "You are an assistant that helps students write essays. You provide detailed outlines and suggestions for improving their writing."
        self.payload = {
            "model": self.MODEL,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": query}
            ],
            "temperature": 0.7
        }

    def create_headers(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.AI_KEY}"
        }

