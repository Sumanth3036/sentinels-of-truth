import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "generated_docs"))
