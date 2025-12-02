import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from database_utils import connect_to_db
from langchain_ollama import ChatOllama, OllamaLLM

from llm import get_final_tables, answer_with_llm
from services.database import db
from services.llm_provider import llm


load_dotenv()


db_name = "AdventureWorksDW2022"
table = "FactProductInventory"


# --------------------------------------
# Get table definitions
# --------------------------------------
def get_table_definitions_for_prompt(
    db: SQLDatabase,
    llm: Any,
    question: str,
) -> str:
    """
    Build the 'database_tables' block for the LLM prompt.

    - If FULL_TABLE_DEFINITION=1 -> return db.table_info (all tables).
    - Else:
        - Use get_final_tables(question) to select relevant tables.
        - For each table, call db.get_table_info(table_names=[table]).
        - Concatenate into a single string.
    """

    full_flag = os.getenv("FULL_TABLE_DEFINITION", "0").strip()

    # ------------------------------------------------------------------
    # FULL MODE: Return all table definitions from the database
    # ------------------------------------------------------------------
    if full_flag == "1":
        # SQLDatabase.table_info is a property that returns a big schema dump
        return db.table_info

    # ------------------------------------------------------------------
    # PARTIAL MODE: Only for final tables decided by the LLM
    # ------------------------------------------------------------------
    final_tables: List[str] = get_final_tables(question, llm)

    if not final_tables:
        # If nothing is returned, fall back to full schema
        # (You can change this to return "" if you prefer strict behavior)
        print("WARNING: get_final_tables returned no tables. Falling back to full schema.")
        return db.table_info

    table_chunks: List[str] = []

    for table_name in final_tables:
        try:
            # get_table_info accepts a list of table names
            info = db.get_table_info(table_names=[table_name])
            if info and info.strip():
                table_chunks.append(info.strip())
        except Exception as e:
            # Non-fatal: skip this table and continue
            print(f"WARNING: Failed to get info for table '{table_name}': {e}")

    if not table_chunks:
        # If all failed, again fallback to full schema
        print("WARNING: No table info could be retrieved. Falling back to full schema.")
        return db.table_info

    # Join each table definition with a blank line between
    return "\n\n".join(table_chunks)



if __name__ == "__main__":
    #question = "Compare Internet and Reseller Sales Amount by calendar year"
    question = "Top 10 customers by latest purchase date"
    database_tables_block = get_table_definitions_for_prompt(db, llm, question)
    final_output = answer_with_llm(database_tables_block, llm, db, db_name, question)

    print(final_output)

    question = "with above list all customers start their name with A"
    database_tables_block = get_table_definitions_for_prompt(db, llm, question)
    final_output = answer_with_llm(database_tables_block, llm, db, db_name, question)

    print(final_output)
    #print(database_tables_block)
