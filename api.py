from fastapi import FastAPI
from pydantic import BaseModel
from llm import get_final_tables, answer_with_llm
from services.database import db
from services.llm_provider import llm
from main import db_name, get_table_definitions_for_prompt

app = FastAPI(title="LangChain NL2SQL Chatbot API")

class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=AnswerResponse)
async def chat_endpoint(payload: QuestionRequest):
    question = payload.question

    # Get table defs (you already have this logic)
    table_block = get_table_definitions_for_prompt(db, llm, question)

    # Run full LLM pipeline
    final_answer = answer_with_llm(table_block, llm, db, db_name, question)

    return AnswerResponse(answer=final_answer)    