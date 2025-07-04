from db_neo4j import get_neo4j_connection

def crear_personaje_en_libro(data):
    """Crea un personaje y lo asocia a un libro en Neo4j"""
    conn = get_neo4j_connection()
    if not conn.connect():
        print("[Neo4j] No se pudo conectar a Neo4j")
        return
    # Crear personaje
    query_personaje = '''
    CREATE (p:Personaje {nombre: $nombre, rol: $rol, casa: $casa, alineacion: $alineacion})
    '''
    conn.execute_query(query_personaje, {
        'nombre': data['nombre'],
        'rol': data['rol'],
        'casa': data['casa'],
        'alineacion': data['alineacion']
    })
    # Crear relación con libro
    query_rel = '''
    MATCH (p:Personaje {nombre: $nombre}), (l:Libro {titulo: $libro})
    MERGE (p)-[:APARECE_EN]->(l)
    '''
    conn.execute_query(query_rel, {
        'nombre': data['nombre'],
        'libro': data['libro']
    })
    print(f"[Neo4j] Personaje '{data['nombre']}' creado y asociado a libro '{data['libro']}'")
    conn.close()

