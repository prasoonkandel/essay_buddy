import os
from dotenv import load_dotenv
from utils.essayGenerator import EssayGenerator
import flet as ft

load_dotenv()

AI_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"
AI_KEY = os.getenv("AI_KEY")
MODEL = "google/gemini-3-flash-preview"

if not AI_KEY:
    raise ValueError("AI_KEY not found in environment variables")

eg = EssayGenerator(AI_KEY, AI_URL, MODEL)

def generate_essay(topic, extra_instructions="", word_count=500):
    if not topic.strip():
        return "Topic cannot be empty."

    try:
        word_count = int(word_count)
    except:
        word_count = 500

    return eg.generateEssay(topic, word_count, extra_instructions)

def main(page: ft.Page):
    page.title = "Essay Generator"
    page.theme_mode = "light"

    topic = ft.TextField(label="Topic", expand=True)
    instructions = ft.TextField(label="Instructions", expand=True)
    word_count = ft.TextField(label="Word Count", value="500", width=150)

    output = ft.TextField(
        label="Generated Essay",
        multiline=True,
        min_lines=10,
        max_lines=20,
        expand=True
    )

    def generate_clicked(e):
        result = generate_essay(
            topic.value,
            instructions.value,
            word_count.value
        )
        output.value = result
        page.update()

    generate_btn = ft.ElevatedButton(
        "Generate Essay",
        on_click=generate_clicked
    )

    page.add(
        ft.Column([
            ft.Text("AI Essay Generator", size=24, weight="bold"),
            topic,
            instructions,
            ft.Row([word_count, generate_btn]),
            output
        ], spacing=15)
    )

ft.app(target=main)