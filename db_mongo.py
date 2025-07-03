import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_DB = os.getenv('MONGO_DB', 'harry_potter')
MONGO_USER = os.getenv('MONGO_USER', 'mongo')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'mongo')


def get_mongo_client():
    """Devuelve un cliente de MongoDB autenticado si corresponde."""
    if MONGO_USER and MONGO_PASSWORD:
        uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
    else:
        uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    return MongoClient(uri)


def get_db():
    """Devuelve la base de datos de trabajo."""
    client = get_mongo_client()
    return client[MONGO_DB]


if __name__ == "__main__":
    try:
        db = get_db()
        print(f"Conexión exitosa a MongoDB. Colecciones disponibles: {db.list_collection_names()}")
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a MongoDB: {e}")
