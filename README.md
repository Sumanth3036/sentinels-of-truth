# Autonomous Document-Generating Agent

FastAPI service that autonomously plans and generates Word (.docx) documents from natural-language business requests.

## Prerequisites

- Python 3.11+
- A free [Groq API key](https://console.groq.com/)

## Setup

1. **Download or clone** this project and open a terminal in the project root.

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   ```bash
   copy .env.example .env       # Windows
   # cp .env.example .env       # macOS/Linux
   ```

   Edit `.env` and set your Groq API key:

   ```
   GROQ_API_KEY=your_actual_groq_key
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

## Run

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive docs: `http://127.0.0.1:8000/docs`

## Test

With the server running, in a second terminal:

```bash
python test_client.py
```

This sends the two required test requests (standard meeting minutes + ambiguous client/platform request), saves JSON responses to `test_outputs/`, and downloads the generated `.docx` files.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/agent` | Body: `{"request": "..."}` → plan, execution log, document path, summary |
| `GET` | `/agent/download/{filename}` | Download a generated `.docx` file |
| `GET` | `/health` | Health check |

## Project structure

```
app/
  config.py     # Environment configuration
  llm.py        # Groq LLM wrapper
  tools.py      # Agent tools (mock data, date, effort estimate)
  planner.py    # Autonomous plan generation
  executor.py   # Plan execution + content drafting
  docgen.py     # Word document generation
main.py         # FastAPI application
test_client.py  # Test script for both required requests
```
