import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_neo4j import get_neo4j_connection

def crear_personaje(conn, nombre, rol, casa, alineacion):
    query = """
    CREATE (:Personaje {
        nombre: $nombre,
        rol: $rol,
        casa: $casa,
        alineacion: $alineacion
    })
    """
    conn.execute_query(query, {
        'nombre': nombre,
        'rol': rol,
        'casa': casa,
        'alineacion': alineacion
    })

def crear_libro(conn, titulo, publicacion, descripcion):
    query = """
    CREATE (:Libro {
        titulo: $titulo,
        publicacion: $publicacion,
        descripcion: $descripcion
    })
    """
    conn.execute_query(query, {
        'titulo': titulo,
        'publicacion': publicacion,
        'descripcion': descripcion
    })

def crear_objeto(conn, nombre, tipo, descripcion):
    query = """
    CREATE (:CosaMagica {
        nombre: $nombre,
        tipo: $tipo,
        descripcion: $descripcion
    })
    """
    conn.execute_query(query, {
        'nombre': nombre,
        'tipo': tipo,
        'descripcion': descripcion
    })

def crear_criatura(conn, nombre):
    query = """
    CREATE (:Criatura {
        nombre: $nombre
    })
    """
    conn.execute_query(query, {'nombre': nombre})

def crear_hechizo(conn, nombre, fecha, evento):
    query = """
    CREATE (:Hechizo {
        nombre: $nombre,
        fecha: $fecha,
        evento: $evento
    })
    """
    conn.execute_query(query, {
        'nombre': nombre,
        'fecha': fecha,
        'evento': evento
    })

def personaje_aparece_en(conn, nombre_personaje, titulo_libro):
    query = """
    MATCH (p:Personaje {nombre: $nombre}), (l:Libro {titulo: $titulo})
    MERGE (p)-[:APARECE_EN]->(l)
    """
    conn.execute_query(query, {
        'nombre': nombre_personaje,
        'titulo': titulo_libro
    })

def objeto_aparece_en(conn, nombre_objeto, titulo_libro):
    query = """
    MATCH (o:CosaMagica {nombre: $nombre}), (l:Libro {titulo: $titulo})
    MERGE (o)-[:APARECE_EN]->(l)
    """
    conn.execute_query(query, {
        'nombre': nombre_objeto,
        'titulo': titulo_libro
    })

def criatura_aparece_en(conn, nombre_criatura, titulo_libro):
    query = """
    MATCH (c:Criatura {nombre: $nombre}), (l:Libro {titulo: $titulo})
    MERGE (c)-[:APARECE_EN]->(l)
    """
    conn.execute_query(query, {
        'nombre': nombre_criatura,
        'titulo': titulo_libro
    })

def personaje_posee_objeto(conn, nombre_personaje, nombre_objeto):
    query = """
    MATCH (p:Personaje {nombre: $nombre}), (o:CosaMagica {nombre: $objeto})
    MERGE (p)-[:POSEE]->(o)
    """
    conn.execute_query(query, {
        'nombre': nombre_personaje,
        'objeto': nombre_objeto
    })

def hechizo_lanzado_con(conn, nombre_hechizo, nombre_objeto):
    query = """
    MATCH (h:Hechizo {nombre: $hechizo}), (o:CosaMagica {nombre: $objeto})
    MERGE (h)-[:LANZADO_CON]->(o)
    """
    conn.execute_query(query, {
        'hechizo': nombre_hechizo,
        'objeto': nombre_objeto
    })

# Seed de ejemplo (ajusta los datos según tu seed de PostgreSQL)
def seed():
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j")
        return

    # Libros
    crear_libro(conn, "La piedra filosofal", 1997, "Primer libro de la saga.")
    crear_libro(conn, "La cámara secreta", 1998, "Segundo libro de la saga.")

    # Personajes
    crear_personaje(conn, "Harry Potter", "Estudiante", "Gryffindor", "Bueno")
    crear_personaje(conn, "Hermione Granger", "Estudiante", "Gryffindor", "Bueno")
    crear_personaje(conn, "Lord Voldemort", "Mago Oscuro", "Slytherin", "Malo")

    # Objetos mágicos
    crear_objeto(conn, "Varita de Saúco", "Varita", "Una de las Reliquias de la Muerte.")
    crear_objeto(conn, "Capa de Invisibilidad", "Capa", "Hace invisible al portador.")

    # Criaturas
    crear_criatura(conn, "Fénix")
    crear_criatura(conn, "Basilisco")

    # Hechizos
    crear_hechizo(conn, "Expelliarmus", "1997-06-26", "Desarma al oponente")
    crear_hechizo(conn, "Avada Kedavra", "1998-07-02", "Maldición asesina")

    # Relaciones
    personaje_aparece_en(conn, "Harry Potter", "La piedra filosofal")
    personaje_aparece_en(conn, "Hermione Granger", "La piedra filosofal")
    personaje_aparece_en(conn, "Lord Voldemort", "La cámara secreta")

    objeto_aparece_en(conn, "Varita de Saúco", "La piedra filosofal")
    objeto_aparece_en(conn, "Capa de Invisibilidad", "La cámara secreta")

    criatura_aparece_en(conn, "Fénix", "La piedra filosofal")
    criatura_aparece_en(conn, "Basilisco", "La cámara secreta")

    personaje_posee_objeto(conn, "Harry Potter", "Capa de Invisibilidad")
    personaje_posee_objeto(conn, "Lord Voldemort", "Varita de Saúco")

    hechizo_lanzado_con(conn, "Expelliarmus", "Varita de Saúco")
    hechizo_lanzado_con(conn, "Avada Kedavra", "Varita de Saúco")

    conn.close()
    print("seed ejecutado")

if __name__ == "__main__":
    seed()
