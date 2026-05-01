import os
from dotenv import load_dotenv
from utils.essayGenerator import EssayGenerator
import flet as ft

load_dotenv()

AI_URL = os.getenv("AI_URL")
AI_KEY = os.getenv("AI_KEY")
AI_MODEL = os.getenv("AI_MODEL")