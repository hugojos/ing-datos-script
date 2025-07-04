import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from neo4j_app.crear import crear_personaje_en_libro, crear_criatura_en_libro, asociar_objeto_magico_a_libro

def seed():
    # Libros
    libros = [
        "LA PIEDRA FILOSOFAL",
        "LA CÁMARA SECRETA",
        "EL PRISIONERO DE AZKABAN",
        "EL CÁLIZ DE FUEGO",
        "LA ORDEN DEL FÉNIX",
        "EL MISTERIO DEL PRÍNCIPE",
        "LAS RELIQUIAS DE LA MUERTE"
    ]
    # Crear nodos de libros explícitamente
    from db_neo4j import get_neo4j_connection
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j para crear libros")
        return
    for idx, libro in enumerate(libros):
        query = """
        MERGE (l:Libro {titulo: $titulo, publicacion: $publicacion, descripcion: $descripcion})
        """
        conn.execute_query(query, {
            'titulo': libro,
            'publicacion': 1997 + idx,  # Asignar año correlativo
            'descripcion': f"Libro {idx+1} de la saga."
        })
    conn.close()
    # Personajes y libros (según seed de PostgreSQL)
    personajes = [
        {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno", "libros": libros},
        {"nombre": "Hermione Granger", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno", "libros": libros[:6]},
        {"nombre": "Ron Weasley", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno", "libros": libros[:5]},
        {"nombre": "Albus Dumbledore", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno", "libros": libros[:5]},
        {"nombre": "Severus Snape", "rol": "profesor", "casa": "Slytherin", "alineacion": "neutral", "libros": libros[1:5]},
        {"nombre": "Draco Malfoy", "rol": "estudiante", "casa": "Slytherin", "alineacion": "neutral", "libros": libros[1:5]},
        {"nombre": "Minerva McGonagall", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno", "libros": libros[:5]},
        {"nombre": "Voldemort", "rol": "villano", "casa": "Slytherin", "alineacion": "malo", "libros": libros[3:]},
    ]
    for p in personajes:
        for libro in p["libros"]:
            crear_personaje_en_libro({
                "nombre": p["nombre"],
                "rol": p["rol"],
                "casa": p["casa"],
                "alineacion": p["alineacion"],
                "libro": libro
            })

    # Criaturas mágicas por libro (según seed de PostgreSQL)
    criaturas = [
        {"nombre": "Buckbeak", "libros": ["EL PRISIONERO DE AZKABAN", "EL CÁLIZ DE FUEGO"]},
        {"nombre": "Fawkes", "libros": ["LA CÁMARA SECRETA", "LA ORDEN DEL FÉNIX"]},
        {"nombre": "Nagini", "libros": ["LAS RELIQUIAS DE LA MUERTE"]},
    ]
    for c in criaturas:
        for libro in c["libros"]:
            crear_criatura_en_libro({
                "nombre": c["nombre"],
                "libro": libro
            })

    # Objetos mágicos y asociación a libros (según seed de PostgreSQL y relaciones Posee/Aparece)
    objetos = [
        {"nombre": "Varita de Saúco", "descripcion": "La varita más poderosa", "tipo": "varita", "personajes": ["Harry Potter", "Albus Dumbledore"]},
        {"nombre": "Varita de Harry", "descripcion": "Varita de acebo", "tipo": "varita", "personajes": ["Ron Weasley"]},
        {"nombre": "Varita de Draco", "descripcion": "Varita de espino", "tipo": "varita", "personajes": ["Severus Snape", "Draco Malfoy"]},
        {"nombre": "Capa de Invisibilidad", "descripcion": "Vuelve invisible", "tipo": "capa", "personajes": ["Harry Potter"]},
        {"nombre": "Horcrux", "descripcion": "Fragmento de alma", "tipo": "objeto", "personajes": ["Voldemort"]},
        {"nombre": "Giratiempos", "descripcion": "Permite viajar en el tiempo", "tipo": "objeto", "personajes": ["Hermione Granger"]},
    ]
    # Para cada objeto, asociarlo a los libros donde el personaje que lo posee aparece
    personaje_libros = {p["nombre"]: p["libros"] for p in personajes}
    for o in objetos:
        libros_objeto = set()
        for personaje in o["personajes"]:
            libros_objeto.update(personaje_libros.get(personaje, []))
        for libro in libros_objeto:
            asociar_objeto_magico_a_libro({
                "nombre": o["nombre"],
                "descripcion": o["descripcion"],
                "tipo": o["tipo"],
                "libro": libro
            })
    print("Seed de Neo4j ejecutado usando solo funciones existentes y datos equivalentes a PostgreSQL.")

if __name__ == "__main__":
    seed()
