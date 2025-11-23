# services/database.py
from langchain_community.utilities import SQLDatabase
from services.config import settings
from database_utils import connect_to_db  

def init_database():
    engine = connect_to_db(settings.DB_NAME)
    db = SQLDatabase(engine)
    return db

db = init_database()


