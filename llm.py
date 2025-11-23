import os
import json
import re

from typing import List, Dict, Any, ClassVar
from dotenv import load_dotenv
from operator import itemgetter

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_ollama import ChatOllama, OllamaLLM
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory

from database_utils import connect_to_db
from llm_prompts import get_system_prompt, get_answer_prompt, get_example_prompt, get_table_details_prompt, get_sql_fix_prompt
from vectorstore_manager import delete_chroma_collection_examples, init_chroma_db_examples, get_similar_examples, debug_list_chroma_items, debug_list_chroma_tables, init_chroma_db_tables, get_similar_tables, delete_chroma_collection_tables
from database_table_descriptions import table_description

load_dotenv()
# Create history object ONCE
history = ChatMessageHistory()



class SQLOnlyParser(BaseOutputParser[str]):
    """
    Bullet-proof SQL extractor:
    - Removes markdown fences
    - Removes explanations
    - Extracts SQL beginning with SELECT/WITH/etc.
    - Stops at the last semicolon
    - Cleans whitespace
    """

    SQL_START: ClassVar = re.compile(
        #r"(SELECT|WITH|INSERT|UPDATE|DELETE|CREATE)\b",
        r"(SELECT|WITH)\b",
        flags=re.IGNORECASE | re.DOTALL
    )

    def parse(self, text: str) -> str:
        # 1. Remove markdown code fences
        text = text.replace("```sql", "").replace("```", "")
        
        # 2. Remove common leading explanations
        text = re.sub(
            r"(?i)(here is|here's|the sql query is|your query is|as requested)[\s\S]*?(SELECT|WITH)",
            r"\2",
            text
        )

        # 3. Locate actual SQL start
        match = self.SQL_START.search(text)
        if not match:
            # No SQL found — fallback to entire text
            return text.strip()

        start = match.start()

        # Text from actual SQL start onward
        sql_part = text[start:]

        # 4. Extract up to first ending semicolon (mandatory SQL terminator)
        end_match = re.search(r";", sql_part)
        if end_match:
            sql_part = sql_part[: end_match.end()]

        # 5. Final cleanup
        sql_part = sql_part.strip()

        # 6. Ensure SQL starts exactly with SELECT/WITH/etc
        # No surrounding whitespace or explanation
        return sql_part


def extract_json_from_llm(result):
    """
    Extract valid JSON regardless of whether the LLM response is:
    - AIMessage (OpenAI, ChatGPT)
    - Raw string (Ollama)
    - JSON inside code blocks
    - Dict-like output
    """

    # 1. If AIMessage → get .content
    if isinstance(result, AIMessage):
        content = result.content
    else:
        content = result

    # 2. If already dict
    if isinstance(content, dict):
        return content

    # 3. If LLM returns list or other JSON structure
    if isinstance(content, (list, tuple)):
        return {"final_tables": list(content)}

    # 4. Must be string from here
    if not isinstance(content, str):
        content = str(content)

    # 5. Strip ```json ... ``` wrappers if present
    code_block_match = re.search(r"```json(.*?)```", content, re.DOTALL)
    if code_block_match:
        content = code_block_match.group(1).strip()

    # 6. Try normal JSON parsing
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # 7. Try extracting { ... } substring
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except:
            pass

    # 8. As final fallback
    print("Unable to parse LLM JSON output")
    print("Raw:", content)
    return {}

def build_prompt(user_question):
    # Fetch best few examples for dynamic few-shot
    fewshot_examples = get_similar_examples(user_question, k=3)
    example_prompt = get_example_prompt()

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=fewshot_examples
    )

    full_prompt = few_shot_prompt.format(input="")
    #full_prompt = fewshot_examples



    return full_prompt



def format_candidate_tables(candidates: List[Dict[str, Any]]) -> str:
    """
    Turn candidate table dicts into a concise text block for the LLM.
    """
    lines = []
    for t in candidates:
        lines.append(
            f"- Table: {t['table']}"
        )
    return "\n".join(lines)

def format_database_tables_from_list(data: List[Dict[str, Any]]) -> str:
    """
    Format list of table JSON objects into a string for LLM prompt.
    """
    lines = []
    for item in data:
        table_name = item["metadata"]["table"]
        description = item["text"]
        lines.append(f"- Table: {table_name}\n Description: {description}")

    return "\n".join(lines)



def get_final_tables(question: str, llm: Any) -> List[str]:
    """
    Returns the list of final tables for a given natural language question.

    Modes:
      - LLM_FIND_TABLE=0 → return only vector-selected tables (k=10)
      - LLM_FIND_TABLE=1 → use LLM to refine selection
    """
    mode = int(os.getenv("LLM_FIND_TABLE", "0"))  # default = vector mode

    # --------------------------------------
    # MODE 0 → Vector Search Only
    # --------------------------------------
    if mode == 0:
        candidate = get_similar_tables(question, k=10)
        return [item["id"] for item in candidate]  # return list of table names

    # --------------------------------------
    # MODE 1 → Vector Search + LLM Refinement
    # --------------------------------------
    # Step 1: vector search (smaller set)
    candidate = get_similar_tables(question, k=5)
    candidate_block = format_candidate_tables(candidate)

    # Step 2: full database descriptions
    # table_description should be a JSON list 
    # Example: load once globally or pass in
    database_tables_block = format_database_tables_from_list(table_description)

    # Step 3: prepare prompt
    prompt = get_table_details_prompt()

    chain = prompt | llm

    result = chain.invoke({
        "question": question,
        "candidate_tables": candidate_block,
        "database_tables": database_tables_block,
        "database": "AdventureWorksDW"
    })

    # LLM returns JSON → parse
    try:
        parsed = extract_json_from_llm(result)
        final_tables = parsed.get("final_tables", [])
        return final_tables
    except Exception as e:
        print("LLM ERROR:", e)
        print("Raw LLM result:", result)
        return []   # fallback behavior

def looks_like_sql_error(text: str) -> bool:
    error_patterns = [
        r"(?i)error", 
        r"(?i)odbc",
        r"(?i)pyodbc",
        r"(?i)incorrect",
        r"(?i)syntax",
        r"(?i)invalid",
        r"(?i)exception",
        r"(?i)fail",
        r"(?i)near",
        r"\b42000\b",  # SQL Server syntax error
        r"\b42S02\b",  # invalid object name
    ]
    return any(re.search(p, text) for p in error_patterns)

def normalize_sql_result(result):
    """
    Normalize SQL execution result safely:
    - Detects real SQL errors
    - Allows stringified valid rows
    """
    # If string → could be error or valid result
    if isinstance(result, str):
        if looks_like_sql_error(result):
            return {"success": False, "data": None, "error": result}
        else:
            # Treat as valid textual result (convert to a data wrapper)
            return {"success": True, "data": result, "error": None}

    # If dict → may contain an "error"
    if isinstance(result, dict):
        if "error" in result:
            return {"success": False, "data": None, "error": result["error"]}
        return {"success": True, "data": result, "error": None}

    # If list → SQL rows -> valid success
    if isinstance(result, list):
        return {"success": True, "data": result, "error": None}

    # Fallback for weird values
    return {"success": False, "data": None, "error": str(result)}


# ---------------------------------------------------------------
# SQL Correction 
# ---------------------------------------------------------------
def run_with_sql_retry(question: str, chain, execute_query, sql_fix_chain, max_retries=5, messages=None,):
    """
    - chain: your generate_query chain
    - execute_query: QuerySQLDataBaseTool(db=db)
    - sql_fix_chain: chain to repair SQL using SQL error
    """
    
    # First attempt — generate SQL normally
    sql = chain.invoke({"question": question,"messages": messages or []})
    
    for attempt in range(max_retries):
        # Try executing SQL
        #result = None
        try:
            #result = execute_query.invoke({"query": sql})
            raw_result = execute_query.invoke({"query": sql})
            # Success case → result is a dict without "error"
            #if "error" not in result:
            #    return sql, result  # return good SQL + good result

        except Exception as e:
            # Hard failure (Python/ODBC error)
            #error_message = str(e)
            raw_result = str(e)

        # If error returned by SQL tool → capture message
        #error_message = result.get("error") if result and "error" in result else error_message
        normalized = normalize_sql_result(raw_result)

        if normalized["success"]:
            return sql, normalized["data"]

        # SQL failed → get error message
        error_message = normalized["error"]

        
        print(f"\n SQL ERROR on attempt {attempt+1}: {error_message}\n")
        print("Retrying with LLM SQL repair...")

        # Ask LLM to fix SQL using the error message
        sql = sql_fix_chain.invoke({
            "sql": sql,
            "error": error_message
        })

    # After all retries fail → return last SQL + error
    return sql, {"error": error_message}




# ---------------------------------------------------------------
# Main Function
# ---------------------------------------------------------------
def answer_with_llm(
    table_definitions: str,
    llm: Any,
    db: SQLDatabase,
    database_name: str,
    question: str,
) -> str:
    """
    Full end-to-end chain:
    1. Build system SQL prompt
    2. Load examples dynamically using vector DB
    3. Build final prompt (system + few-shot + human)
    4. Create SQL generation chain
    5. Execute query → get result
    6. Rephrase answer using final LLM step
    7. Return final human-friendly answer
    """

    # -----------------------------------------------------------
    # 1. SYSTEM PROMPT
    # -----------------------------------------------------------
    system_prompt = get_system_prompt(
        database=database_name,
        dialect=db.dialect,
        database_table_details=table_definitions,
        top_k=5,
    )

    sql_fix_prompt = get_sql_fix_prompt(
        database_table_details=table_definitions,
    )

   
    # -----------------------------------------------------------
    # 2. FEW-SHOT EXAMPLES (Dynamic from Vector Store)
    # -----------------------------------------------------------
    example_prompt = get_example_prompt()
    fewshot_examples = get_similar_examples(question, k=4)

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=fewshot_examples,
    )


    # -----------------------------------------------------------
    # 3. COMBINE SYSTEM + FEWSHOT + HUMAN PROMPT
    # -----------------------------------------------------------
    final_prompt = ChatPromptTemplate.from_messages(
        [
            system_prompt,             # now a ChatPromptTemplate with all static vars bound
            few_shot_prompt,                      # OK, stays as-is
            MessagesPlaceholder(variable_name="messages"), 
            ("human", "{question}"),              # human message
        ]
    )

    sql_fix_chat_prompt = ChatPromptTemplate.from_messages(
        [
            sql_fix_prompt,             # now a ChatPromptTemplate with all static vars bound
            ("human", "Previous SQL:\n{sql}\n\nError Message:\n{error}\n\nReturn corrected SQL:"),              # human message
        ]
    )

    # -----------------------------------------------------------
    # 4. SQL GENERATION CHAIN
    # -----------------------------------------------------------
    generate_query = final_prompt | llm | SQLOnlyParser()
    sql_fix_chain = sql_fix_chat_prompt | llm | SQLOnlyParser()


    # -------------------------------------------------------
    # 5) SQL EXECUTION TOOL
    # -------------------------------------------------------
    execute_query = QuerySQLDataBaseTool(db=db)
    # This expects {"query": "<SQL>"} when used in a chain with itemgetter.

    # -------------------------------------------------------
    # 6) REPHRASE ANSWER CHAIN
    # -------------------------------------------------------
    answer_prompt_template = get_answer_prompt()
    rephrase_answer_chain = answer_prompt_template | llm | StrOutputParser()
    # This expects keys: question, query, result

    # -------------------------------------------------------
    # 7) FULL CHAIN
    # -------------------------------------------------------
    
    sql, result = run_with_sql_retry(
        question=question,
        chain=generate_query,
        execute_query=execute_query,
        sql_fix_chain=sql_fix_chain,
        max_retries=int(os.getenv("MAX_RETRIES", "3")),   # configurable
        messages=history.messages
    )
    

    final_answer = rephrase_answer_chain.invoke({
        "question": question,
        "query": sql,
        "result": result
    })

    # -----------------------------------------------------------
    # ADD USER MESSAGE TO HISTORY
    # -----------------------------------------------------------
    history.add_user_message(question)
    history.add_ai_message(final_answer)

    return final_answer




if __name__ == "__main__":
    question = "Top 5 products by internet sales?"
    prompt = build_prompt(question)

    print("\n--- FINAL PROMPT SENT TO LLAMA3 ---\n")
    print(prompt)
    #print(format_database_tables_from_list(table_description))
    #print(format_candidate_tables(get_similar_tables(question, k=5)))
    #print(get_final_tables(question))



