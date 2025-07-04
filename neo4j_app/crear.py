import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_neo4j import limpiar_base_datos, crear_indices
from rich.console import Console
from rich.panel import Panel

console = Console()

def crear_base_neo4j():
    """Elimina todos los nodos y relaciones de Neo4j y recrea los índices."""
    try:
        limpiar_base_datos()
        crear_indices()
        console.print(Panel("[bold green]Base de datos Neo4j reiniciada y lista para poblar.[/bold green]", title="Neo4j Crear"))
    except Exception as e:
        console.print(Panel(f"[bold red]Error al crear la base de datos Neo4j: {e}[/bold red]", title="Error"))

if __name__ == "__main__":
    crear_base_neo4j()
