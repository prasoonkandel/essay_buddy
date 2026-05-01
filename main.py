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

def generate_essay(topic, word_count=500, extra_instructions=""):
    if not topic.strip():
        return "Topic cannot be empty."

    try:
        word_count = int(word_count)
    except:
        word_count = 500

    return eg.generateEssay(topic, word_count, extra_instructions)

def main(page: ft.Page):
    page.title = "Essay Buddy"
    page.theme_mode = "system"
    page.window_width = 1280
    page.window_height = 720
    page.padding = 20

    page.theme = ft.Theme(
        color_scheme_seed="indigo",
        use_material3=True
    )
    page.dark_theme = ft.Theme(
        color_scheme_seed="deepPurple",
        use_material3=True
    )

    topic = ft.TextField(label="Topic", expand=True)

    word_count = ft.Dropdown(
        label="Word Count",
        width=200,
        options=[
            ft.dropdown.Option("250"),
            ft.dropdown.Option("500"),
            ft.dropdown.Option("750"),
            ft.dropdown.Option("1000"),
        ],
        value="500"
    )

    extra_check = ft.Checkbox(label="Add extra instructions")

    instructions = ft.TextField(
        label="Extra Instructions",
        multiline=True,
        visible=False
    )

    loader = ft.ProgressRing(visible=False)
    generating_text = ft.Text("Generating...", visible=False, size=16, weight="bold")

    output = ft.TextField(
        label="Generated Essay",
        multiline=True,
        min_lines=15,
        read_only=True,
        visible=False,
        expand=True
    )

    def toggle_extra(e):
        instructions.visible = extra_check.value
        page.update()

    extra_check.on_change = toggle_extra
    
    if extra_check.value:
            instructions.visible = True
            page.update()

    def generate_clicked(e):

        generate_btn.disabled = True
        topic.disabled = True
        word_count.disabled = True
        extra_check.disabled = True
        instructions.disabled = True
        loader.visible = True
        generating_text.visible = True
        page.update()
        page.update()

        wc = int(word_count.value)

        extra_text = instructions.value if extra_check.value else ""

        result = generate_essay(topic.value, wc, extra_text)

        output.value = result
        output.visible = True
        loader.visible = False
        generating_text.visible = False
        generate_btn.disabled = False
        topic.disabled = False
        word_count.disabled = False
        extra_check.disabled = False
        instructions.disabled = False
        generating_text.visible = False
        loader.visible = False
        page.update()
        page.update()

    generate_btn = ft.ElevatedButton(
        "Generate Essay",
        icon="auto_awesome",
        on_click=generate_clicked
    )
            

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
            ft.Text("Essay Buddy", size=28, weight="bold"),

            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        topic,
                        word_count,
                        extra_check,
                        instructions, 
                        ft.Row([generate_btn, loader, generating_text])
                    ], spacing=15)
                )
            ),

                ft.Card(
                    content=ft.Container(
                        padding=20,
                        content=output,
                        expand=True
                    )
                )
            ], spacing=20)
        )
    

ft.app(target=main)