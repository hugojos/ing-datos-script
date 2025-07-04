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

def crear_estructura_base():
    """Crea la estructura básica de la base de datos con algunos datos de ejemplo"""
    print("creando estructura básica")
    
    try:
        neo4j_conn = get_neo4j_connection()
        if neo4j_conn.connect():
            consultas_ejemplo = [
                """
                CREATE (h:Hechizo {
                    nombre: 'Expelliarmus',
                    descripcion: 'Desarmador',
                    dificultad: 'Intermedio',
                    tipo: 'Defensivo'
                })
                """,
                """
                CREATE (p:Personaje {
                    nombre: 'Harry Potter',
                    casa: 'Gryffindor',
                    sangre: 'Mestiza',
                    ocupacion: 'Estudiante'
                })
                """,
                """
                CREATE (o:ObjetoMagico {
                    nombre: 'Varita de Saúco',
                    descripcion: 'La varita más poderosa que existe',
                    rareza: 'Única',
                    origen: 'Desconocido'
                })
                """
            ]
            for consulta in consultas_ejemplo:
                neo4j_conn.execute_query(consulta)
            print("estructura básica creada con datos de ejemplo")
        neo4j_conn.close()
        print("Neo4j poblada con datos de ejemplo.")
    except Exception as e:
        print(f"Error al crear estructura base: {e}")

def main():
    """Función principal que ejecuta el reset completo"""
    reset_neo4j()

if __name__ == "__main__":
    main()
