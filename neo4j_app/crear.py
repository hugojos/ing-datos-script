def asociar_objeto_magico_a_libro(data):
    """Crea un objeto mágico (CosaMagica) y lo asocia a un libro en Neo4j."""
    from db_neo4j import get_neo4j_connection
    conn = get_neo4j_connection()
    if not conn.connect():
        print("[Neo4j] No se pudo conectar a Neo4j")
        return
    # Crear objeto mágico (si no existe)
    query_objeto = '''
    MERGE (o:CosaMagica {nombre: $nombre, descripcion: $descripcion, tipo: $tipo})
    '''
    conn.execute_query(query_objeto, {'nombre': data['nombre'], 'descripcion': data.get('descripcion', ''), 'tipo': data.get('tipo', 'general')})
    # Crear relación con libro
    query_rel = '''
    MATCH (o:CosaMagica {nombre: $nombre}), (l:Libro {titulo: $libro})
    MERGE (o)-[:APARECE_EN]->(l)
    '''
    conn.execute_query(query_rel, {'nombre': data['nombre'], 'libro': data['libro']})
    print(f"[Neo4j] Objeto mágico '{data['nombre']}' creado y asociado a libro '{data['libro']}'")
    conn.close()
def crear_criatura_en_libro(data):
    """Crea una criatura mágica y la asocia a un libro en Neo4j"""
    from db_neo4j import get_neo4j_connection
    conn = get_neo4j_connection()
    if not conn.connect():
        print("[Neo4j] No se pudo conectar a Neo4j")
        return
    # Crear criatura (si no existe)
    query_criatura = '''
    MERGE (c:CriaturaMagica {nombre: $nombre})
    '''
    conn.execute_query(query_criatura, {'nombre': data['nombre']})
    # Crear relación con libro
    query_rel = '''
    MATCH (c:CriaturaMagica {nombre: $nombre}), (l:Libro {titulo: $libro})
    MERGE (c)-[:MENCIONADA_EN]->(l)
    '''
    conn.execute_query(query_rel, {'nombre': data['nombre'], 'libro': data['libro']})
    print(f"[Neo4j] Monstruo '{data['nombre']}' creado y asociado a libro '{data['libro']}'")
    conn.close()
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

