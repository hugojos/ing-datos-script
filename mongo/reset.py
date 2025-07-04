
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_mongo import get_db
import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()

def reset_libros():
    db = get_db()
    db.libros.delete_many({})
    print("------- MongoDB reset -------")
    print("colección 'libros' reseteada")
    # Ejecutar seed.py automáticamente
    try:
        subprocess.run(["py", "mongo/seed.py"], check=True)
        print("seed ejecutado")
    except Exception as e:
        print(f"No se pudo ejecutar seed.py automáticamente: {e}")

if __name__ == "__main__":
    reset_libros()
