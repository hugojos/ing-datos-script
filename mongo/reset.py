
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
    console.print(Panel("[bold green]Colección 'libros' reseteada correctamente.[/bold green]", title="MongoDB Reset"))
    # Ejecutar seed.py automáticamente
    try:
        subprocess.run(["py", "mongo/seed.py"], check=True)
        console.print(Panel("[bold green]Colección 'libros' poblada correctamente (seed.py ejecutado).[/bold green]", title="MongoDB Seed"))
    except Exception as e:
        console.print(Panel(f"[bold red]No se pudo ejecutar seed.py automáticamente: {e}[/bold red]", title="Error"))

if __name__ == "__main__":
    reset_libros()
