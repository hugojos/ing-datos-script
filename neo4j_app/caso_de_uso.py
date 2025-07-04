import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_neo4j import get_neo4j_connection

def caso_1():
    """Personajes por libro"""
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j")
        return
    query = '''
    MATCH (p:Personaje)-[:APARECE_EN]->(l:Libro)
    RETURN l.titulo AS libro, COUNT(DISTINCT p) AS cantidad_personajes
    ORDER BY cantidad_personajes DESC
    '''
    result = conn.execute_query(query)
    from rich.table import Table
    from rich.console import Console
    table = Table(title="Personajes por libro (Neo4j)")
    table.add_column("Libro", style="cyan")
    table.add_column("Cantidad de personajes", style="magenta")
    for row in result:
        table.add_row(str(row.get('libro', '')), str(row.get('cantidad_personajes', '')))
    Console().print(table)
    conn.close()

def caso_2():
    """Objetos más relevantes"""
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j")
        return
    query = '''
    MATCH (o:CosaMagica)-[:APARECE_EN]->(l:Libro)
    RETURN o.nombre AS objeto, COUNT(DISTINCT l) AS cantidad_libros
    ORDER BY cantidad_libros DESC
    '''
    result = conn.execute_query(query)
    from rich.table import Table
    from rich.console import Console
    table = Table(title="Objetos más relevantes (Neo4j)")
    table.add_column("Objeto", style="cyan")
    table.add_column("Cantidad de libros", style="magenta")
    for row in result:
        table.add_row(str(row.get('objeto', '')), str(row.get('cantidad_libros', '')))
    Console().print(table)
    conn.close()

def caso_3():
    """Criaturas por libro"""
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j")
        return
    query = '''
    MATCH (l:Libro)
    OPTIONAL MATCH (c:Criatura)-[:APARECE_EN]->(l)
    RETURN l.titulo AS libro, COLLECT(DISTINCT c.nombre) AS criaturas
    ORDER BY l.publicacion
    '''
    result = conn.execute_query(query)
    from rich.table import Table
    from rich.console import Console
    table = Table(title="Criaturas por libro (Neo4j)")
    table.add_column("Libro", style="cyan")
    table.add_column("Criaturas", style="magenta")
    for row in result:
        criaturas = ', '.join([c for c in row.get('criaturas', []) if c]) if row.get('criaturas') else '-'
        table.add_row(str(row.get('libro', '')), criaturas)
    Console().print(table)
    conn.close()

def caso_4():
    """Profesores que aparecen en más de 4 libros"""
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j")
        return
    query = '''
    MATCH (p:Personaje)-[:APARECE_EN]->(l:Libro)
    WHERE p.rol = 'profesor'
    WITH p, COUNT(DISTINCT l) AS libros_aparece
    WHERE libros_aparece > 4
    RETURN p.nombre AS personaje, libros_aparece
    '''
    result = conn.execute_query(query)
    from rich.table import Table
    from rich.console import Console
    table = Table(title="Profesores en más de 4 libros (Neo4j)")
    table.add_column("Personaje", style="cyan")
    table.add_column("Libros en los que aparece", style="magenta")
    for row in result:
        table.add_row(str(row.get('personaje', '')), str(row.get('libros_aparece', '')))
    Console().print(table)
    conn.close()

def caso_5():
    """Objetos mencionados o poseídos por personajes buenos en el último libro"""
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j")
        return
    query = '''
    MATCH (o1:CosaMagica)-[:APARECE_EN]->(:Libro {titulo: "Las Reliquias de la Muerte"})
    WITH COLLECT(DISTINCT o1) AS objetos_del_ultimo
    MATCH (p:Personaje {alineacion: "bueno"})-[:POSEE]->(o2:CosaMagica)
    WITH objetos_del_ultimo + COLLECT(DISTINCT o2) AS todos_los_objetos
    UNWIND todos_los_objetos AS objeto
    RETURN COUNT(DISTINCT objeto) AS total_objetos
    '''
    result = conn.execute_query(query)
    from rich.table import Table
    from rich.console import Console
    table = Table(title="Objetos mencionados o poseídos (Neo4j)")
    table.add_column("Total de objetos", style="magenta")
    for row in result:
        table.add_row(str(row.get('total_objetos', '')))
    Console().print(table)
    conn.close()

def caso_6():
    """Varita y hechizo más usado"""
    conn = get_neo4j_connection()
    if not conn.connect():
        print("No se pudo conectar a Neo4j")
        return
    query = '''
    MATCH (p:Personaje)-[:POSEE]->(o:CosaMagica)
    WHERE o.nombre CONTAINS "Varita"
    WITH o, COUNT(DISTINCT p) AS cantidad_duenios
    ORDER BY cantidad_duenios DESC
    LIMIT 1
    WITH o AS varita_elegida
    MATCH (h:Hechizo)-[:LANZADO_CON]->(varita_elegida)
    WITH varita_elegida, h, COUNT(*) AS veces_usado
    ORDER BY veces_usado DESC
    LIMIT 1
    RETURN varita_elegida.nombre AS varita, h.nombre AS hechizo, veces_usado
    '''
    result = conn.execute_query(query)
    from rich.table import Table
    from rich.console import Console
    table = Table(title="Varita y hechizo más usado (Neo4j)")
    table.add_column("Varita", style="cyan")
    table.add_column("Hechizo", style="magenta")
    table.add_column("Veces usado", style="green")
    for row in result:
        table.add_row(str(row.get('varita', '')), str(row.get('hechizo', '')), str(row.get('veces_usado', '')))
    Console().print(table)
    conn.close()
