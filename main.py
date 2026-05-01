import os
from dotenv import load_dotenv
from utils.essayGenerator import EssayGenerator
import flet as ft

load_dotenv()

AI_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"
AI_KEY = os.getenv("AI_KEY")
MODEL = "google/gemini-3-flash-preview"