# NL2SQLAgent
NL2SQLAgent


✨ NL2SQLAgent – Natural Language to SQL Chatbot (Prototype)
📘 Project Brief

NL2SQLAgent is a prototype Natural Language → SQL chatbot that converts user questions into SQL queries and retrieves answers directly from a SQL Server database.

The system is built on a Retrieval-Augmented Generation (RAG) architecture using LangChain, and supports both local LLMs (Ollama) and OpenAI LLMs.

🏗️ High-Level System Architecture

The NL2SQL pipeline consists of the following key components:

1️⃣ Candidate Table Selection (Semantic Search)

User input → Semantic similarity search against DB Table Descriptions
→ returns candidate tables closely related to the question.

2️⃣ Final Table Selection using LLM

LLM receives:
✔ user question
✔ candidate tables
✔ table descriptions
✔ environment variables that enable/disable table filtering
→ returns final list of tables to use for SQL.

3️⃣ Schema Extraction

Database schemas are extracted for all final tables.

4️⃣ Few-Shot Retrieval (Example-Based RAG)

Semantic similarity search retrieves the top 3 example SQL templates
(from a vector store populated from sql_examples.py).

5️⃣ SQL Generation with LLM

LLM receives:
✔ user question
✔ table schemas
✔ example SQLs
✔ chat history
✔ system constraints
→ Generates SQL.

6️⃣ SQL Execution

Generated SQL is executed directly on the database.

7️⃣ Error Correction Loop (Self-Healing SQL)

If SQL execution fails:

Error message sent back to LLM

SQL auto-corrected

Up to 5 retry attempts (configurable via .env)

8️⃣ Natural Language Result Conversion

Raw SQL results → passed through LLM → converted to a clean natural-language answer.

9️⃣ Multi-LLM Support

The system can run using:

Ollama (local LLMs such as llama3, mixtral, nous-hermes)

OpenAI API (e.g., gpt-4o-mini)

🚀 How to Run the Project
✅ 1. Install Local MS SQL Server

You must have SQL Server running locally with the AdventureWorksDW2022 database restored.

✅ 2. Create VectorDB for SQL Examples

Run the following Python function:

from vectorstore_manager import init_chroma_db_examples
init_chroma_db_examples()


This loads examples from sql_examples.py into chroma_few_shot/.

✅ 3. Create VectorDB for Table Descriptions

Run:

from vectorstore_manager import init_chroma_db_tables
init_chroma_db_tables()


This loads DB metadata from database_table_descriptions.py into chroma_tables/.

✅ 4. Start FastAPI Backend

From project root:

uvicorn api:app --reload


FastAPI runs at:

👉 http://localhost:8000

✅ 5. Start Streamlit Frontend
streamlit run frontend/streamlit_app.py


This opens a web UI for chat-based SQL querying.

🔐 Environment Configuration (.env)

Create a .env file at the project root with the following structure:

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=

# SQL Server connection info
SQL_SERVER=localhost
SQL_USERNAME=   # or leave blank for Windows auth
SQL_PASSWORD=   # optional
SQL_DRIVER=ODBC Driver 17 for SQL Server
DATABASE_NAME=

# Ollama LLM model names
OLLAMA_LLM=llama3
#OLLAMA_LLM=nous-hermes2-mixtral

OLLAMA_EMBEDDING=nomic-embed-text

# Vector store directories
PERSIST_DIR=chroma_few_shot
COLLECTION_NAME=few_shot_examples
TABLE_PERSIST_DIR=chroma_tables
TABLE_COLLECTION_NAME=adw_tables

# LLM logic controls
LLM_FIND_TABLE=1
FULL_TABLE_DEFINITION=0
MAX_RETRIES=5

# OpenAI settings
ENABLE_OPENAI_API=1
OPENAI_API_KEY=
#OPENAI_LLM=gpt-3.5-turbo
OPENAI_LLM=gpt-4o-mini

📦 Tech Stack
Component	Technology
Backend	FastAPI
Frontend	Streamlit
RAG Engine	LangChain, ChromaDB
SQL Execution	SQLAlchemy + MS SQL Server
LLM Providers	Ollama, OpenAI
Embeddings	Nomic / OpenAI Embeddings
Chat Memory	LangChain ChatMessageHistory
📁 Project Highlights

Few-shot example retrieval using vector similarity

Table selection + schema filtering

Multi-turn chat history

Self-healing SQL generation with retry loop

Supports multiple LLM providers

Works offline using Ollama

Clean modular design (backend + frontend)