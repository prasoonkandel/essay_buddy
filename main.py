import requests
import json 
import os
from dotenv import load_dotenv
from utils.essayGenerator import EssayGenerator

load_dotenv()

AI_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"

AI_KEY = os.getenv("AI_KEY")

MODEL = "google/gemini-3-flash-preview"


EG = EssayGenerator(AI_KEY, AI_URL, MODEL)

query = input("Enter the topic for the essay: ")

essay = EG.generateEssay(query)

print(essay)



    