
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_neo4j import limpiar_base_datos, crear_indices


def crear_base_neo4j():
    """Elimina todos los nodos y relaciones de Neo4j y recrea los índices."""
    try:
        limpiar_base_datos()
        crear_indices()
        print("------- Neo4j Reset -------")
        print("Base de datos Neo4j limpiada exitosamente")
    except Exception as e:
        print("------- Error -------")
        print(f"Error al resetear la base de datos Neo4j: {e}")

if __name__ == "__main__":
    crear_base_neo4j()
