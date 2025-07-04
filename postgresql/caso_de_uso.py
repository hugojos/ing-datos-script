def caso_1():
    from rich.table import Table
    from rich.console import Console
    import os
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    import time
    start = time.perf_counter()
    cur.execute('''
        SELECT p.titulo AS libro, COUNT(DISTINCT a.personaje_id) AS cantidad_personajes
        FROM Publicacion p
        JOIN Aparece a ON a.publicacion_id = p.id
        GROUP BY p.id, p.titulo
        ORDER BY p.id
    ''')
    elapsed = (time.perf_counter() - start) * 1000
    rows = cur.fetchall()
    table = Table(title="Personajes por libro")
    table.add_column("Libro", style="cyan")
    table.add_column("Cantidad de personajes", style="magenta")
    for libro, cantidad in rows:
        table.add_row(str(libro), str(cantidad))
    Console().print(table)
    Console().print(f"[green]Consulta ejecutada en {elapsed:.2f} ms[/green]")
    cur.close()
    conn.close()
def caso_2():
    from rich.table import Table
    from rich.console import Console
    import os
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    import time
    start = time.perf_counter()
    cur.execute('''
        SELECT o.nombre, COUNT(DISTINCT pub.id) AS cantidad_libros
        FROM ObjetoMagico o
        JOIN Posee po ON po.objeto_id = o.id
        JOIN Aparece a ON a.personaje_id = po.personaje_id
        JOIN Publicacion pub ON pub.id = a.publicacion_id
        WHERE pub.tipo = 'libro'
        GROUP BY o.id, o.nombre
        ORDER BY cantidad_libros DESC
    ''')
    elapsed = (time.perf_counter() - start) * 1000
    rows = cur.fetchall()
    table = Table(title="Objetos mágicos por cantidad de libros")
    table.add_column("Objeto", style="cyan")
    table.add_column("Cantidad de libros", style="magenta")
    for nombre, cantidad in rows:
        table.add_row(str(nombre), str(cantidad))
    Console().print(table)
    Console().print(f"[green]Consulta ejecutada en {elapsed:.2f} ms[/green]")
    cur.close()
    conn.close()
def caso_3():
    from rich.table import Table
    from rich.console import Console
    import os
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    import time
    start = time.perf_counter()
    cur.execute('''
        SELECT pu.titulo AS libro, STRING_AGG(cm.nombre, ', ') AS criaturas
        FROM CriaturaMagica cm
        JOIN Mencion m ON m.criatura_id = cm.id
        JOIN Publicacion pu ON m.publicacion_id = pu.id
        GROUP BY pu.titulo
        ORDER BY pu.titulo
    ''')
    elapsed = (time.perf_counter() - start) * 1000
    rows = cur.fetchall()
    from rich.table import Table
    from rich.panel import Panel
    table = Table(title="Criaturas por libro")
    table.add_column("Libro", style="cyan")
    table.add_column("Criaturas", style="magenta")
    vacio = True
    for libro, criaturas in rows:
        vacio = False
        table.add_row(str(libro), str(criaturas) if criaturas else '-')
    if vacio:
        Console().print(Panel("No se encontraron resultados.", title="Sin datos", style="red"))
    else:
        Console().print(table)
    Console().print(f"[green]Consulta ejecutada en {elapsed:.2f} ms[/green]")
    cur.close()
    conn.close()
def caso_4():
    from rich.table import Table
    from rich.console import Console
    import os
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    import time
    start = time.perf_counter()
    cur.execute('''
        SELECT pe.nombre, COUNT(DISTINCT a.publicacion_id) AS cantidad_libros
        FROM Personaje pe
        JOIN Aparece a ON pe.id = a.personaje_id
        WHERE pe.rol = 'profesor'
        GROUP BY pe.id, pe.nombre
        HAVING COUNT(DISTINCT a.publicacion_id) > 4
    ''')
    elapsed = (time.perf_counter() - start) * 1000
    rows = cur.fetchall()
    from rich.table import Table
    from rich.panel import Panel
    table = Table(title="Profesores que aparecen en más de 4 libros")
    table.add_column("Profesor", style="cyan")
    table.add_column("Cantidad de libros", style="magenta")
    vacio = True
    for nombre, cantidad in rows:
        vacio = False
        table.add_row(str(nombre), str(cantidad))
    if vacio:
        Console().print(Panel("No se encontraron resultados.", title="Sin datos", style="red"))
    else:
        Console().print(table)
    Console().print(f"[green]Consulta ejecutada en {elapsed:.2f} ms[/green]")
    cur.close()
    conn.close()
def caso_5():
    from rich.console import Console
    import os
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    import time
    start = time.perf_counter()
    cur.execute('''
        WITH ultimo_libro AS (
            SELECT id FROM Publicacion ORDER BY ano_lanzamiento DESC LIMIT 1
        ),
        objetos_ultimo_libro AS (
            SELECT DISTINCT po.objeto_id
            FROM Posee po
            JOIN Aparece a ON po.personaje_id = a.personaje_id
            WHERE a.publicacion_id = (SELECT id FROM ultimo_libro)
        ),
        objetos_personajes_buenos AS (
            SELECT DISTINCT po.objeto_id
            FROM Posee po
            JOIN Personaje pe ON po.personaje_id = pe.id
            WHERE pe.alineacion = 'bueno'
        )
        SELECT COUNT(DISTINCT objeto_id) AS cantidad_objetos
        FROM (
            SELECT objeto_id FROM objetos_ultimo_libro
            UNION
            SELECT objeto_id FROM objetos_personajes_buenos
        ) AS union_resultado;
    ''')
    elapsed = (time.perf_counter() - start) * 1000
    row = cur.fetchone()
    cantidad = row[0] if row else 0
    from rich.table import Table
    table = Table(title="Cantidad de objetos mágicos únicos")
    table.add_column("Cantidad", style="magenta")
    table.add_row(str(cantidad))
    Console().print(table)
    Console().print(f"[green]Consulta ejecutada en {elapsed:.2f} ms[/green]")
    cur.close()
    conn.close()
def caso_6():
    from rich.console import Console
    from rich.table import Table
    import os
    import psycopg2
    from dotenv import load_dotenv
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    import time
    start = time.perf_counter()
    cur.execute('''
        WITH varita_mas_usada AS (
            SELECT o.id AS varita_id, COUNT(DISTINCT po.personaje_id) AS cantidad_personajes
            FROM ObjetoMagico o
            JOIN Posee po ON po.objeto_id = o.id
            WHERE o.tipo = 'varita'
            GROUP BY o.id
            ORDER BY cantidad_personajes DESC
            LIMIT 1
        ),
        personaje_con_varita AS (
            SELECT po.personaje_id
            FROM Posee po
            JOIN varita_mas_usada vm ON vm.varita_id = po.objeto_id
            LIMIT 1
        )
        SELECT h.nombre AS hechizo_mas_usado, a.veces_usado
        FROM Aprende a
        JOIN personaje_con_varita pcv ON pcv.personaje_id = a.personaje_id
        JOIN Hechizo h ON h.id = a.hechizo_id
        ORDER BY a.veces_usado DESC
        LIMIT 1;
    ''')
    elapsed = (time.perf_counter() - start) * 1000
    row = cur.fetchone()
    from rich.table import Table
    from rich.panel import Panel
    if row:
        hechizo, veces = row
        table = Table(title="Hechizo más usado por varitas")
        table.add_column("Hechizo", style="cyan")
        table.add_column("Cantidad de usos", style="magenta")
        table.add_row(str(hechizo), str(veces))
        Console().print(table)
    else:
        Console().print(Panel("No se encontraron resultados.", title="Sin datos", style="red"))
    Console().print(f"[green]Consulta ejecutada en {elapsed:.2f} ms[/green]")
    cur.close()
    conn.close()
