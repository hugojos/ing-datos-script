import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self.driver = None
        
    def connect(self):
        """Establece conexión con Neo4j"""
        try:
            uri = f"bolt://{os.getenv('NEO4J_HOST', 'localhost')}:{os.getenv('NEO4J_PORT', '7687')}"
            username = os.getenv('NEO4J_USER', 'neo4j')
            password = os.getenv('NEO4J_PASSWORD', 'neo4j123')
            
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            return True
        except Exception as e:
            print(f"Error al conectar con Neo4j: {e}")
            return False
    
    def close(self):
        """Cierra la conexión con Neo4j"""
        if self.driver:
            self.driver.close()
    
    def execute_query(self, query, parameters=None):
        """Ejecuta una consulta en Neo4j"""
        if not self.driver:
            if not self.connect():
                return None
        
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return result.data()
        except Exception as e:
            print(f"Error al ejecutar consulta: {e}")
            return None

def get_neo4j_connection():
    """Devuelve una instancia de conexión Neo4j"""
    return Neo4jConnection()

def test_neo4j_connection():
    """Prueba la conexión a Neo4j"""
    try:
        neo4j_conn = get_neo4j_connection()
        if neo4j_conn.connect():
            # Probar con una consulta simple
            result = neo4j_conn.execute_query("RETURN 1 as test")
            if result:
                print("Conexión exitosa a Neo4j")
                print(f"Resultado de prueba: {result}")
            else:
                print("Conexión establecida pero no se pudo ejecutar consulta de prueba")
        else:
            print("No se pudo establecer conexión con Neo4j")
        neo4j_conn.close()
    except Exception as e:
        print(f"Error al probar conexión Neo4j: {e}")

def crear_indices():
    """Crea índices para optimizar las consultas"""
    try:
        neo4j_conn = get_neo4j_connection()
        if neo4j_conn.connect():
            # Crear índices para los nodos principales
            indices = [
                "CREATE INDEX personaje_nombre IF NOT EXISTS FOR (p:Personaje) ON (p.nombre)",
                "CREATE INDEX hechizo_nombre IF NOT EXISTS FOR (h:Hechizo) ON (h.nombre)",
                "CREATE INDEX objeto_magico_nombre IF NOT EXISTS FOR (o:ObjetoMagico) ON (o.nombre)",
                "CREATE INDEX publicacion_titulo IF NOT EXISTS FOR (p:Publicacion) ON (p.titulo)",
                "CREATE INDEX criatura_magica_nombre IF NOT EXISTS FOR (c:CriaturaMagica) ON (c.nombre)"
            ]
            
            for indice in indices:
                neo4j_conn.execute_query(indice)
            
            pass  # Eliminado mensaje de índices creados exitosamente
        neo4j_conn.close()
    except Exception as e:
        print(f"Error al crear índices: {e}")

def limpiar_base_datos():
    """Limpia completamente la base de datos Neo4j"""
    try:
        neo4j_conn = get_neo4j_connection()
        if neo4j_conn.connect():
            # Eliminar todos los nodos y relaciones
            neo4j_conn.execute_query("MATCH (n) DETACH DELETE n")
            # El mensaje se moverá a crear.py después de '------- Neo4j Reset -------'
        neo4j_conn.close()
    except Exception as e:
        print(f"Error al limpiar base de datos: {e}")

def obtener_estadisticas():
    """Obtiene estadísticas de la base de datos"""
    try:
        neo4j_conn = get_neo4j_connection()
        if neo4j_conn.connect():
            # Contar nodos por tipo
            consultas = [
                ("Personajes", "MATCH (n:Personaje) RETURN count(n) as count"),
                ("Hechizos", "MATCH (n:Hechizo) RETURN count(n) as count"),
                ("Objetos Mágicos", "MATCH (n:ObjetoMagico) RETURN count(n) as count"),
                ("Publicaciones", "MATCH (n:Publicacion) RETURN count(n) as count"),
                ("Criaturas Mágicas", "MATCH (n:CriaturaMagica) RETURN count(n) as count"),
                ("Total Relaciones", "MATCH ()-[r]->() RETURN count(r) as count")
            ]
            
            print("\n=== Estadísticas de Neo4j ===")
            for nombre, consulta in consultas:
                result = neo4j_conn.execute_query(consulta)
                if result:
                    count = result[0]['count']
                    print(f"{nombre}: {count}")
                else:
                    print(f"{nombre}: Error al obtener dato")
        neo4j_conn.close()
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")

if __name__ == "__main__":
    test_neo4j_connection()
