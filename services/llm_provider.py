# services/llm_provider.py
import os
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from services.config import settings

def init_llm():
    if settings.ENABLE_OPENAI:
        print("Using OpenAI LLM")
        return ChatOpenAI(
            model=settings.OPENAI_LLM,
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
    else:
        print("Using Ollama LLM")
        return OllamaLLM(
            model=settings.OLLAMA_LLM,
            temperature=0
        )

llm = init_llm()
