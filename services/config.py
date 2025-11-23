# services/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DB_NAME = os.getenv("DATABASE_NAME", "AdventureWorksDW2022")

    # LLM Provider Settings
    ENABLE_OPENAI = os.getenv("ENABLE_OPENAI_API", "0") == "1"

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_LLM = os.getenv("OPENAI_LLM", "gpt-4o-mini")

    # Ollama
    OLLAMA_LLM = os.getenv("OLLAMA_LLM", "llama3")

settings = Settings()
