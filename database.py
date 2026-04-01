import pickle, os
from config import DB_FILE
def guardar_db(db):
    with open(DB_FILE, "wb") as f: pickle.dump(db, f)
def cargar_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f: return pickle.load(f)
    return {}