import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, inspect

load_dotenv()

def get_connection_string(database_name: str) -> str:
    """Create a SQLAlchemy connection string for the given DB."""
    
    server = os.getenv("SQL_SERVER", "localhost")
    driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    username = os.getenv("SQL_USERNAME", "")
    password = os.getenv("SQL_PASSWORD", "")

    # Windows Auth
    if username == "" and password == "":
        return f"mssql+pyodbc://@{server}/{database_name}?driver={driver}&trusted_connection=yes"

    # SQL Auth
    return f"mssql+pyodbc://{username}:{password}@{server}/{database_name}?driver={driver}"


def connect_to_db(database_name: str):
    """Return SQLAlchemy engine connection."""
    conn_str = get_connection_string(database_name)
    return create_engine(conn_str)


def get_dialect(database_name: str):
    """Return SQL dialect information."""
    engine = connect_to_db(database_name)
    return engine.dialect.name


def list_tables(database_name: str):
    """List all tables in the database."""
    engine = connect_to_db(database_name)
    inspector = inspect(engine)
    return inspector.get_table_names()


def get_table_schema(database_name: str, table_name: str):
    """Return schema (columns + types) for a specific table."""
    engine = connect_to_db(database_name)
    inspector = inspect(engine)
    return inspector.get_columns(table_name)


def get_full_schema(database_name: str):
    """Return schema for every table in the database."""
    engine = connect_to_db(database_name)
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    schema = {}

    for table in tables:
        schema[table] = inspector.get_columns(table)

    return schema

def get_inspector(database_name: str):
    """Return SQLAlchemy inspector for the database."""
    engine = connect_to_db(database_name)
    return inspect(engine)


def get_table_columns(database_name: str, table_name: str):
    inspector = get_inspector(database_name)
    return inspector.get_columns(table_name)


def get_primary_keys(database_name: str, table_name: str):
    inspector = get_inspector(database_name)
    pk_info = inspector.get_pk_constraint(table_name)
    return pk_info.get("constrained_columns", [])


def get_foreign_keys(database_name: str, table_name: str):
    inspector = get_inspector(database_name)
    return inspector.get_foreign_keys(table_name)


def get_table_full_schema(database_name: str, table_name: str):
    """
    Returns complete information:
    - Columns
    - Primary Keys
    - Foreign Keys
    """
    return {
        "columns": get_table_columns(database_name, table_name),
        "primary_keys": get_primary_keys(database_name, table_name),
        "foreign_keys": get_foreign_keys(database_name, table_name)
    }


if __name__ == "__main__":
    db_name = "AdventureWorksDW2022"
    table = "FactProductInventory"
    print(f"Connection String: {get_connection_string(db_name)}")

    print("Dialect:", get_dialect(db_name))
    print("Tables:", list_tables(db_name))

    print(f"\n--- Table Schema: {table} ---")
    print(get_table_schema(db_name, table))

    print("\n--- FULL SCHEMA ---")
    print(get_full_schema(db_name))


    print("\n=== COLUMNS ===")
    for c in get_table_columns(db_name, table):
        print(f"{c['name']} - {c['type']} (nullable={c['nullable']})")

    print("\n=== PRIMARY KEYS ===")
    print(get_primary_keys(db_name, table))

    print("\n=== FOREIGN KEYS ===")
    print(get_foreign_keys(db_name, table))

    print("\n=== FULL SCHEMA ===")
    print(get_table_full_schema(db_name, table))
