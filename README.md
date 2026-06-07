# Essay Buddy

A simple AI assistant which can help you write essays.

![Fork Repo](https://github.com/prasoonkandel/notes_cpp/fork)

## Features

- Generates an essay on your desired topic.
- Lets you choose the length of essay according to your need.
- You provide additional description if you want.
- Responsive UI and design.
- Beautiful custom cursor and cursor nimation in UI.
- Felxible backend if want to use this locally.

## Project Setup Guide:

1. Clone the repository

```bash
git clone https://github.com/prasoonkandel/essay_buddy.git
cd essay_buddy
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

```bash
cd frontend
npm install
```

3. Configure environment

Create a `.env` file in the project root and add:

```env
AI_URL=https://your-ai-provider-endpoint
AI_KEY=your_api_key_here
AI_MODEL=your_model_name
```

Create a `.env` file in the frontend dir and add:

```env
API_BASE_URL=https://your-backend-url.com/
# Example: http://localhost:5000/
```

4. Run the app (new terminal)

```bash
python app.py
```

5. Run frontend (new terminal)

```bash
cd frontend
npm run dev
```

### Built By Prasoon Kandel
