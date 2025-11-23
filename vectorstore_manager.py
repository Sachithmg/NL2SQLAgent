import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

from sql_examples import examples
from database_table_descriptions import table_description


load_dotenv()

# -----------------------------
# CONFIG
# -----------------------------
ollama_embedding = os.getenv("OLLAMA_EMBEDDING")

chroma_fewshot_persist_dir = os.getenv("PERSIST_DIR")
chroma_fewshot_collection = os.getenv("COLLECTION_NAME")

chroma_tables_persist_dir = os.getenv("TABLE_PERSIST_DIR")
chroma_tables_collection = os.getenv("TABLE_COLLECTION_NAME")


embeddings = OllamaEmbeddings(model=ollama_embedding)
BEST_EXAMPLES = examples



# ----------------------------------------------------------
# DELETE COLLECTION FUNCTION (Requested)
# ----------------------------------------------------------
def delete_chroma_collection_examples():
    """
    Deletes the entire Chroma collection and clears the physical DB directory.
    Fully compatible with langchain-chroma.
    Safe to call even if the collection does not exist.
    """
    print("Deleting Chroma collection...")

    # Initialize vectorstore client
    try:
        vectorstore = Chroma(
            collection_name=chroma_fewshot_collection,
            embedding_function=embeddings,
            persist_directory=chroma_fewshot_persist_dir,
        )
    except Exception as e:
        print(f"Failed to initialize Chroma: {e}")
        return

    # Try deleting collection safely
    try:
        vectorstore.reset_collection()
        print("Collection deleted/reset successfully.")
    except Exception as e:
        print(f"Warning: Collection could not be deleted or already removed.\n{e}")

    # Clean physical folder
    if os.path.exists(chroma_fewshot_persist_dir):
        try:
            for file in os.listdir(chroma_fewshot_persist_dir):
                path = os.path.join(chroma_fewshot_persist_dir, file)
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    import shutil
                    shutil.rmtree(path)
            print("Physical Chroma DB folder cleaned.")
        except Exception as e:
            print(f"Failed cleaning directory: {e}")

    print("Chroma DB fully reset.")




# ----------------------------------------------------------
# Create Chroma DB if missing, else load existing
# ----------------------------------------------------------
def init_chroma_db_examples():
    """
    Initialize or load Chroma DB in a safe way for langchain-chroma.
    Avoids reset_collection() bug when the DB already exists.
    """
    db_exists = os.path.exists(chroma_fewshot_persist_dir)

    # Always initialize embeddings first
    print("Initializing Chroma with embeddings...")

    # Step 1: Create Chroma instance
    vectorstore = Chroma(
        collection_name=chroma_fewshot_collection,
        embedding_function=embeddings,
        persist_directory=chroma_fewshot_persist_dir
    )

    # Step 2: If DB does not exist → create collection & seed
    if not db_exists:
        print("Creating new Chroma DB and seeding examples...")

        vectorstore.reset_collection()  # SAFE only for first-time creation

        texts = [ex["input"] for ex in BEST_EXAMPLES]
        metadatas = [{"query": ex["query"]} for ex in BEST_EXAMPLES]

        vectorstore.add_texts(texts=texts, metadatas=metadatas)

        print("DB created and seeded.")
        return vectorstore

    # Step 3: DB exists → check if collection is empty or uninitialized
    print("Loading existing Chroma DB...")

    try:
        data = vectorstore._collection.get(include=["documents"])
        doc_count = len(data["documents"]) if data["documents"] else 0
    except Exception:
        doc_count = 0

    if doc_count == 0:
        print("Collection exists but EMPTY or UNINITIALIZED -> reseeding...")

        vectorstore.reset_collection()

        texts = [ex["input"] for ex in BEST_EXAMPLES]
        metadatas = [{"query": ex["query"]} for ex in BEST_EXAMPLES]

        vectorstore.add_texts(texts=texts, metadatas=metadatas)

        print("Collection fixed and seeded.")
    else:
        print(f"Existing collection loaded with {doc_count} documents.")

    return vectorstore



# ----------------------------------------------------------
# Retrieve best matching examples for a given question
# ----------------------------------------------------------
def get_similar_examples(question: str, k: int = 3):
    """
    Returns top-k semantically similar examples from Chroma.
    """
    vectorstore = Chroma(
        collection_name=chroma_fewshot_collection,
        embedding_function=embeddings,
        persist_directory=chroma_fewshot_persist_dir
    )

    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=k,
        input_keys=["input"]
    )

    selected_meta = example_selector.select_examples({"input": question})

    # Fetch full Chroma documents
    raw = vectorstore._collection.get(include=["documents", "metadatas"])

    # Build lookup map from "query" to {"input", "query"}
    items = []
    for doc, meta in zip(raw["documents"], raw["metadatas"]):
        # doc == input text, meta["query"] == SQL
        items.append({"input": doc, "query": meta["query"]})

    # Now match metadata.query to full example
    final = []
    for m in selected_meta:
        for item in items:
            if item["query"] == m["query"]:
                final.append(item)
                break

    return final
    return selected



def debug_list_chroma_items():
    """
    Print all stored texts + metadata inside the Chroma DB.
    """
    vectorstore = Chroma(
        collection_name=chroma_fewshot_collection,
        embedding_function=embeddings,
        persist_directory=chroma_fewshot_persist_dir
    )

    collection = vectorstore._collection

    # Get all ids, documents, and metadata
    items = collection.get(include=["metadatas", "documents"])

    print("\n Chroma DB Content:")
    for i, doc in enumerate(items["documents"]):
        print(f"\n---- RECORD {i+1} ----")
        print("Document:", doc)
        print("Metadata:", items["metadatas"][i])
        print("----------------------")
    
    print("\nTotal records:", len(items["documents"]))



# =============================================================
# DELETE COLLECTION
# =============================================================
def delete_chroma_collection_tables():
    """
    Deletes entire Chroma collection + physical folder.
    """
    print("Deleting Chroma TABLES collection...")

    try:
        vectorstore = Chroma(
            collection_name=chroma_tables_collection,
            embedding_function=embeddings,
            persist_directory=chroma_tables_persist_dir
        )
    except Exception as e:
        print(f"Init failed: {e}")
        return

    try:
        vectorstore.reset_collection()
        print("Chroma tables collection reset.")
    except Exception as e:
        print("Warning (reset):", e)

    # Delete folder
    import shutil
    if os.path.exists(chroma_tables_persist_dir):
        shutil.rmtree(chroma_tables_persist_dir, ignore_errors=True)
        print("Physical folder removed.")

    print("Chroma TABLES DB fully cleared.")

# =============================================================
# INIT / LOAD TABLE CHROMA DB
# =============================================================
def init_chroma_db_tables():
    """
    Initializes the Chroma vector DB for tables.
    If DB does not exist → create + seed.
    If exists but empty → reseed.
    If exists with data → load only.
    """
    db_exists = os.path.exists(chroma_tables_persist_dir)

    print("Initializing TABLE Chroma DB...")

    vectorstore = Chroma(
        collection_name=chroma_tables_collection,
        embedding_function=embeddings,
        persist_directory=chroma_tables_persist_dir,
    )

    # New DB or missing folder
    if not db_exists:
        print("Creating new TABLE collection and seeding...")
        vectorstore.reset_collection()
        load_tables_into_chroma(vectorstore)
        print(f"Seeded {len(table_description)} tables into Chroma.")
        return vectorstore

    # DB exists → check document count
    try:
        data = vectorstore._collection.get(include=["documents"])
        doc_count = len(data["documents"]) if data["documents"] else 0
    except:
        doc_count = 0

    if doc_count == 0:
        print("Existing TABLE collection is EMPTY → reseeding...")
        vectorstore.reset_collection()
        load_tables_into_chroma(vectorstore)
        print(f"Reseeded {len(table_description)} table entries.")
    else:
        print(f"Loaded TABLE Chroma DB with {doc_count} items.")

    return vectorstore

# =============================================================
# LOAD TABLE DATASET INTO CHROMA
# =============================================================
def load_tables_into_chroma(vectorstore: Chroma):
    """
    Adds the AdventureWorks table metadata entries to Chroma.
    """
    texts = [t["text"] for t in table_description]
    metadatas = [t["metadata"] for t in table_description]
    ids = [t["id"] for t in table_description]
    vectorstore.add_texts(texts=texts, metadatas=metadatas, ids=ids)




# =============================================================
# TABLE RETRIEVAL
# =============================================================
def get_similar_tables(question: str, k: int = 5):
    """
    Returns the top-k most relevant AdventureWorksDW tables for a question.
    Always returns: id, table_name, text.
    """
    vectorstore = Chroma(
        collection_name=chroma_tables_collection,
        embedding_function=embeddings,
        persist_directory=chroma_tables_persist_dir
    )

    selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=k,
        input_keys=["input"]
    )

    selected = selector.select_examples({"input": question})

    # Fetch full documents from Chroma
    raw = vectorstore._collection.get(include=["documents", "metadatas"])

    # Build lookup by TABLE NAME (metadata)
    lookup = {}
    for i in range(len(raw["documents"])):
        table_name = raw["metadatas"][i]["table"]       # e.g., "DimProduct"
        lookup[table_name] = {
            "id": raw["ids"][i],
            "table": table_name,
            "text": raw["documents"][i]
        }

    # Now match selected tables to full lookup
    final = []
    for sel in selected:
        table_name = sel["table"]        # selector returns this from metadata
        if table_name in lookup:
            final.append(lookup[table_name])

    return final


# =============================================================
# DEBUG LISTING
# =============================================================
def debug_list_chroma_tables():
    vectorstore = Chroma(
        collection_name=chroma_tables_collection,
        embedding_function=embeddings,
        persist_directory=chroma_tables_persist_dir
    )


    items = vectorstore._collection.get(include=["documents", "metadatas"])

    print("\n===== TABLE VECTOR STORE CONTENT =====")
    for idx, doc in enumerate(items["documents"]):
        print(f"\n--- TABLE #{idx + 1} ---")
        print("Id:", items["ids"][idx])
        print("Text:", doc)
        print("Metadata:", items["metadatas"][idx])
    print(f"\nTotal: {len(items['documents'])} table entries.")

if __name__ == "__main__":
    #delete_chroma_collection_examples()
    #init_chroma_db_examples()
    #debug_list_chroma_items()
    # question = "Top 5 products by internet sales?"
    # fewshot_examples = get_similar_examples(question, k=3)
    print("\n--- Examples from Chroma ---\n")
    # print(fewshot_examples)

    #delete_chroma_collection_tables()
    #init_chroma_db_tables()
    #print(get_similar_tables( "Top 5 products by internet sales?",  10))
    #debug_list_chroma_tables()



