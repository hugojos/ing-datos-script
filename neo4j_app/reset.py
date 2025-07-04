import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_neo4j import get_neo4j_connection, limpiar_base_datos, crear_indices, obtener_estadisticas
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

def reset_neo4j():
    """Resetea completamente la base de datos Neo4j"""
    try:
        limpiar_base_datos()
        crear_indices()
        print("------- Neo4j Reset -------")
        print("Base de datos Neo4j limpiada exitosamente")
        return True
    except Exception as e:
        print("------- Error -------")
        print(f"Error al resetear la base de datos Neo4j: {e}")
        return False

def main():
    """Función principal que ejecuta el reset completo"""
    reset_neo4j()

if __name__ == "__main__":
    main()
