from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

def get_system_prompt(database: str, dialect: str, database_table_details: str, top_k: int = 5) :
    """
    Returns a LangChain PromptTemplate configured with the correct SQL prompt.
    """
    
    template = """
    You are an expert SQL query generator. You work strictly with the {database} database using the {dialect} SQL dialect.

    Your job is to produce ONE SINGLE SQL query that correctly answers the user’s question.

    IMPORTANT RULES:

    1. Never join fact tables at the detail level, even if they share keys through a common dimension (e.g., both have OrderDateKey).
    2. Fact tables must be joined only to dimension tables.
    3. When a query needs measures from multiple fact tables (e.g., FactInternetSales and FactResellerSales):
        a. Aggregate each fact table separately at the required grain (e.g., per DateKey, or per DateKey + CustomerKey + ProductKey).
        b. Then outer join these aggregated result sets on their shared dimension keys (e.g., DateKey, CustomerKey).
        c. Use a dimension table (e.g., DimDate) as the driving table, and LEFT JOIN each aggregated fact result to it to avoid losing rows.
    4. Do not write queries like:
        FROM FactInternetSales fis JOIN FactResellerSales frs ON fis.OrderDateKey = frs.OrderDateKey
    5. This can create a Cartesian product at the date grain (N×M rows), which overstates SUM() measures.
    6. Instead, write queries using CTEs or subqueries that aggregate each fact first, and then join those aggregates via dimensions.
    7. NEVER use tables or columns not present in the schema.
    8. NEVER perform DML operations (INSERT, UPDATE, DELETE, MERGE, DROP, TRUNCATE).
    You are allowed to generate only SELECT queries.
    9. ALWAYS generate syntactically correct SQL for the {dialect} engine.
    10. If the user does not request a specific number of results, limit the query to {top_k} rows.
    11. NEVER select all columns. Select only columns needed to answer the question.
    12. ALWAYS double-check the query for:
    - valid table names
    - valid join keys
    - correct aggregation
    - correct filtering
    - correct date columns
    - correct GROUP BY usage
    13. NEVER include explanations, markdown, commentary, or text outside the SQL.
    14. ALWAYS start the output directly with:
    SELECT
    (no leading spaces, no comments)
    15. Output must be EXACTLY ONE SQL statement. No surrounding quotes.
    16. If multiple tables appear in the join path, choose the shortest correct join path.

    DATABASE SCHEMA (read carefully before generating SQL):
    {database_table_details}
    """

    # Create ChatPromptTemplate and bind static values
    prompt = ChatPromptTemplate.from_messages(
        [("system", template)]
    )

    # Bind everything EXCEPT {question}
    return prompt.partial(
        database=database,
        dialect=dialect,
        database_table_details=database_table_details,
        top_k=top_k,
    )
   


def get_answer_prompt() -> PromptTemplate :
    
    template = """
    You are a data assistant. Answer the question strictly based on the SQL Result.

    Rules:
    - Only use the SQL Result to answer.
    - Do not guess. If data is missing or empty, answer "No results found."
    - Keep the answer short and factual.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}

    Answer:
    """
    return PromptTemplate.from_template(template)


# Prompt template for each example
def get_example_prompt() -> ChatPromptTemplate:
    template = [
         ("human", "{input}\nSQLQuery:"),
         ("ai", "{query}"),
     ]
    return ChatPromptTemplate.from_messages(template)


def get_table_details_prompt() -> PromptTemplate:
    template = """
    You are an expert data warehouse SQL assistant working with the {database} star schema.

    User question:
    {question}

    Candidate tables identified via vector search:
    {candidate_tables}

    Full list of database tables with descriptions:
    {database_tables}

    Your task:
    1. Identify all tables that are potentially relevant to the user question.
    2. Always include the main fact table(s) containing measures.
    3. Include any dimension tables required for joins, filtering, or grouping (e.g., DimDate, DimCustomer, DimProduct, DimSalesTerritory, DimPromotion), even if they were not in the candidate list.
    4. Ensure join paths are complete using foreign key relationships.
    5. You MUST only use table names exactly as they appear in the database list.
    6. You MUST return **only a JSON object** and nothing else. No explanation. No commentary. No text before or after.
    7. Your output MUST start with  '{{' and end with '}}'.
    8. If you are unsure, include the table anyway.

    Return JSON in the following exact format (escape braces shown below):

    {{
    "final_tables": [
        "FactInternetSales",
        "DimDate",
        "DimCustomer"
    ]
    }}

    Requirements:
    - Output ONLY valid JSON.
    - No additional text outside the JSON object.
    """
    return PromptTemplate.from_template(template)


def get_sql_fix_prompt(database_table_details: str)-> PromptTemplate:
    template = """
    You are an SQL repair assistant.
    Given a faulty SQL query and the database error message, fix ONLY the SQL.
    Return ONLY corrected SQL. No explanations. No markdown.

    DATABASE SCHEMA (read carefully before generating SQL):
    {database_table_details}
    """
    # Create ChatPromptTemplate and bind static values
    prompt = ChatPromptTemplate.from_messages(
        [("system", template)]
    )

    # Bind everything EXCEPT {question}
    return prompt.partial(
        database_table_details=database_table_details,
    )

if __name__ == "__main__":
    print(get_system_prompt("testDB", 10))