import json
import glob
import os
import re
import math

from difflib import SequenceMatcher

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_core.messages import AIMessage, HumanMessage

from llm import run_with_sql_retry, get_similar_examples, SQLOnlyParser
from llm_prompts import get_system_prompt, get_sql_fix_prompt, get_example_prompt
from main import db_name, get_table_definitions_for_prompt
from services.database import db
from services.llm_provider import llm




def load_validation_tasks(folder="validation"):
    tasks = []
    for file in glob.glob(os.path.join(folder, "*.json")):
        with open(file, "r") as f:
            data = json.load(f)
            tasks.extend(data)
    return tasks


def get_model_sql(question, database_name, db, llm, table_definitions):


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
    # 7) FULL CHAIN
    # -------------------------------------------------------
    
    sql, result = run_with_sql_retry(
        question=question,
        chain= generate_query,            # your generate_query chain
        execute_query=execute_query,
        sql_fix_chain=sql_fix_chain,
        max_retries=3,
        messages=[]  # no history for batch eval
    )
    return sql, result


def map_columns(model_cols, gold_cols):
    mapping = {}
    for m in model_cols:
        best_match = None
        best_score = 0
        for g in gold_cols:
            score = SequenceMatcher(None, m.lower(), g.lower()).ratio()
            if score > best_score:
                best_score = score
                best_match = g
        mapping[m] = best_match
    return mapping





def detect_key_column(model_rows, gold_rows):
    if not model_rows or not gold_rows:
        return None
    
    model_keys = model_rows[0].keys()
    gold_keys = gold_rows[0].keys()

    for mk in model_keys:
        for gk in gold_keys:
            # If values overlap significantly, treat as join key
            m_vals = {r[mk] for r in model_rows}
            g_vals = {r[gk] for r in gold_rows}
            overlap = len(m_vals & g_vals)
            if overlap >= min(len(m_vals), len(g_vals)) * 0.5:
                return mk, gk

    return None

def row_to_values(row):
    """Convert row dict → sorted list of comparable values."""
    vals = list(row.values())
    # Normalize decimals, numbers, strings
    norm = []
    for v in vals:
        if v is None:
            norm.append(None)
        else:
            try:
                norm.append(float(v))
            except:
                norm.append(str(v).strip())
    # Sorting improves position-insensitive matching
    return sorted(norm, key=lambda x: (str(type(x)), str(x)))





def compare_rows_semantic(model_row, gold_row):
    score_list = []
    
    for key in gold_row:
        if key not in model_row:
            continue
        
        v1 = model_row[key]
        v2 = gold_row[key]

        # identical
        if v1 == v2:
            score_list.append(1.0)
            continue

        # numeric?
        try:
            n1 = float(v1)
            n2 = float(v2)
            diff = abs(n1 - n2) / (abs(n2) + 1e-9)
            score_list.append(max(0, 1 - diff))
            continue
        except:
            pass

        # fuzzy string match
        score_list.append(SequenceMatcher(None, str(v1), str(v2)).ratio())

    if not score_list:
        return 0.0

    return sum(score_list) / len(score_list)


def execute_gold_sql(db, gold_sql):
    try:
        tool = QuerySQLDataBaseTool(db=db)
        result = tool.invoke({"query": gold_sql})
        return True, result, None
    except Exception as e:
        return False, None, str(e)
    
def normalize_sql(sql):
    sql = sql.lower()
    sql = re.sub(r"\s+", " ", sql)
    return sql.strip()

def sql_similarity(model_sql, gold_sql):
    m = normalize_sql(model_sql)
    g = normalize_sql(gold_sql)

    # Levenshtein (sequence match)
    ratio = SequenceMatcher(None, m, g).ratio()

    # Token overlap (Jaccard)
    m_tokens = set(m.split())
    g_tokens = set(g.split())
    jaccard = len(m_tokens & g_tokens) / len(m_tokens | g_tokens)

    # Combined score
    return (ratio * 0.6) + (jaccard * 0.4)



def compare_rows(r1, r2, tolerance=0.0001):
    """
    Compares two rows (dicts) with numeric tolerance.
    Returns score between 0 and 1.
    """

    keys1 = set(r1.keys())
    keys2 = set(r2.keys())
    col_score = len(keys1 & keys2) / len(keys1 | keys2)

    value_scores = []
    for k in (keys1 & keys2):
        v1, v2 = r1[k], r2[k]

        # exact match (strings, dates)
        if v1 == v2:
            value_scores.append(1.0)
            continue

        # numeric comparison
        try:
            n1, n2 = float(v1), float(v2)
            if n1 == 0 and n2 == 0:
                value_scores.append(1.0)
            else:
                diff = abs(n1 - n2) / (abs(n2) + 1e-9)
                value_scores.append(max(0, 1 - diff))
        except:
            # fallback: partial string similarity
            value_scores.append(SequenceMatcher(None, str(v1), str(v2)).ratio())

    if not value_scores:
        return col_score

    return (col_score * 0.3) + (sum(value_scores)/len(value_scores) * 0.7)


def normalize_result(res):
    """
    Convert any SQL result into a list.
    Handles:
    - list
    - dict with "data"
    - tuple
    - single row
    - None
    - error strings
    """

    if res is None:
        return []

    # Case: error string → no data
    if isinstance(res, str):
        return []

    # Case: already list
    if isinstance(res, list):
        return res

    # Case: dict from SQL tool
    if isinstance(res, dict):
        if "data" in res and isinstance(res["data"], list):
            return res["data"]
        return []

    # Case: a single tuple row (convert to list of 1 row)
    if isinstance(res, tuple):
        return [res]

    # Case: unknown type
    return []

def normalize_row(row):
    if isinstance(row, dict):
        return list(row.values())
    if isinstance(row, tuple) or isinstance(row, list):
        return list(row)
    return []

def compare_value_lists(a, b, tol=0.0001):
    if len(a) != len(b):
        return 0.0
    matches = 0
    for x, y in zip(a, b):
        if values_equal(x, y, tol):
            matches += 1
    return matches / len(a)

def values_equal(x, y, tol=0.0001):
    from decimal import Decimal

    # Numeric compare with tolerance
    try:
        dx = Decimal(str(x))
        dy = Decimal(str(y))
        return abs(dx - dy) <= Decimal(str(tol))
    except:
        pass

    # String compare
    return str(x).strip().lower() == str(y).strip().lower()


def result_similarity(model_res, gold_res):
    """
    Value-based comparison of SQL results.
    Works when results are:
    - list of tuples
    - list of dicts
    - list of lists
    - single row tuple
    - single row dict
    - dict containing "data"
    """

    # -----------------------------------------------------
    # 1. Auto-normalize inputs into list form
    # -----------------------------------------------------
    model_res = normalize_result(model_res)
    gold_res = normalize_result(gold_res)

    # If still not lists → mismatch
    if not isinstance(model_res, list) or not isinstance(gold_res, list):
        return 0.0

    # Empty set logic
    if len(model_res) == 0 and len(gold_res) == 0:
        return 1.0
    if len(gold_res) == 0:
        return 0.0

    # -----------------------------------------------------
    # 2. Normalize rows to pure value lists
    # -----------------------------------------------------
    model_vals = [normalize_row(r) for r in model_res]
    gold_vals = [normalize_row(r) for r in gold_res]

    # -----------------------------------------------------
    # 3. Compare using best-match per gold row
    # -----------------------------------------------------
    row_scores = []
    for g in gold_vals:
        best = max(compare_value_lists(g, m) for m in model_vals)
        row_scores.append(best)

    return sum(row_scores) / len(row_scores)

def llm_result_validation(llm, model_res, gold_res):
    prompt = f"""
    You are validating SQL query results from a text-to-SQL model.

    GOLD RESULT:
    {gold_res}

    MODEL RESULT:
    {model_res}

    Return ONLY a decimal similarity score between 0 and 1 based on:
    - Whether values represent the same meaning
    - Whether aggregations match
    - Whether totals differ by small numerical margins
    - Whether column mappings represent equivalent logic

    Do NOT output anything else.
    """

    reply = llm.invoke([HumanMessage(content=prompt)]).content

    try:
        score = float(reply.strip())
    except:
        score = 0.0

    return max(0, min(1, score))


def final_similarity(model_sql, gold_sql, model_res, gold_res, llm=None):
    sql_score = sql_similarity(model_sql, gold_sql)
    val_score = result_similarity(model_res, gold_res)

    # LLM semantic score (optional)
    llm_score = llm_result_validation(llm, model_res, gold_res) if llm else 0.0

    # Weighted combination
    final = (sql_score * 0.2) + (val_score * 0.6) + (llm_score * 0.2)

    return {
        "sql_similarity": sql_score,
        "value_similarity": val_score,
        "llm_similarity": llm_score,
        "final_score": final,
        "final_pass": final > 0.70
    }



def update_json_file(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)




def evaluate_dataset(folder="validation", llm=None, output_file="validation_results.json"):
    """
    Loads all validation tasks, evaluates models, 
    and writes updated JSON including final similarity scores.
    """

    tasks = load_validation_tasks(folder)
    results = []   # <-- collect all updated tasks

    for task in tasks:
        question = task["question"]
        gold_sql = task["gold_sql"]
        task_id = task["id"]

        print(f"\n🔍 Evaluating ID={task_id}: {question}")

        # Safe defaults before processing
        safe_result = {
            "model_sql": None,
            "validated": True,
            "model_exec_ok": False,
            "result_match": False,
            "gold_error": None,
            "model_error": None,
            "sql_similarity": 0.0,
            "value_similarity": 0.0,
            "llm_similarity": 0.0,
            "final_score": 0.0,
            "final_pass": False,
        }

        try: 

            table_block = get_table_definitions_for_prompt(db, llm, question)

            # ---------------------------------------------------
            # 1) Generate SQL with model
            # ---------------------------------------------------
            model_sql, model_res = get_model_sql(
                question=question,
                database_name=db_name,
                db=db,
                llm=llm,
                table_definitions=table_block  # precomputed earlier
            )

            # ---------------------------------------------------
            # 2) Execute gold SQL
            # ---------------------------------------------------
            gold_ok, gold_res, gold_error = execute_gold_sql(db, gold_sql)

            # ---------------------------------------------------
            # 3) Compute similarities
            # ---------------------------------------------------
            sql_score = sql_similarity(model_sql, gold_sql)

            value_score = result_similarity(
                model_res,
                gold_res if gold_ok else []
            )

            llm_score = (
                llm_result_validation(llm, model_res, gold_res)
                if llm else 0.0
            )

            final_score = (sql_score * 0.2) + (value_score * 0.4) + (llm_score * 0.4)
            final_pass = final_score >= 0.70

            # ---------------------------------------------------
            # 4. Update safe result
            # ---------------------------------------------------
            safe_result.update({
                "model_sql": model_sql,
                "model_exec_ok": isinstance(model_res, list),
                "result_match": value_score > 0.70,
                "gold_error": gold_error,
                "model_error": None if isinstance(model_res, list) else str(model_res),
                "sql_similarity": sql_score,
                "value_similarity": value_score,
                "llm_similarity": llm_score,
                "final_score": final_score,
                "final_pass": final_pass,
            })


                   
            print(
                f"SQL={sql_score:.2f}, Value={value_score:.2f}, "
                f"LLM={llm_score:.2f}, Final={final_score:.2f}, Pass={final_pass}"
            )

        except Exception as e:
                    # ---------------------------------------------------
                    # Exception handling per task
                    # ---------------------------------------------------
                    print(f"❌ ERROR processing task {task_id}: {e}")

                    safe_result["model_error"] = str(e)
                    safe_result["final_pass"] = False

        # ---------------------------------------------------
        # Always append result & continue loop
        # ---------------------------------------------------
        task.update(safe_result)
        results.append(task)

    # ---------------------------------------------------
    # FINAL WRITE ( ALWAYS RUNS )
    # ---------------------------------------------------
    output_path = os.path.join(folder, output_file)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        print(f"\n🎉 All test results written to: {output_path}")

    except Exception as e:
        print(f"❌ Failed to write final results file: {e}")     





if __name__ == "__main__":
    evaluate_dataset("validation", llm, "validation_results_2.json")


