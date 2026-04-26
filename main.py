import requests
import json 
import os
from dotenv import load_dotenv

load_dotenv()

AI_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"

AI_KEY = os.getenv("AI_KEY")


    