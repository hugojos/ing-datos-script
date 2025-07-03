import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_mongo import get_db
import subprocess

def reset_libros():
    db = get_db()
    db.libros.delete_many({})
    print("Colección 'libros' reseteada correctamente.")
    # Ejecutar seed.py automáticamente
    try:
        subprocess.run(["py", "mongo/seed.py"], check=True)
        print("Colección 'libros' poblada correctamente (seed.py ejecutado).")
    except Exception as e:
        print(f"[ERROR] No se pudo ejecutar seed.py automáticamente: {e}")

if __name__ == "__main__":
    reset_libros()
