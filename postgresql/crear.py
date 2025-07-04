def asociar_objeto_magico_a_libro(data):
    """Crea un objeto mágico (si no existe) y lo asocia a un libro en PostgreSQL, usando un personaje genérico si es necesario."""
    import os
    from dotenv import load_dotenv
    import psycopg2
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        # Crear objeto mágico si no existe (no insertar id manualmente)
        cur.execute("SELECT id FROM objetomagico WHERE nombre = %s", (data["nombre"],))
        row = cur.fetchone()
        if row:
            objeto_id = row[0]
        else:
            cur.execute("INSERT INTO objetomagico (nombre, descripcion, tipo) VALUES (%s, %s, %s) RETURNING id", (data["nombre"], data.get("descripcion", ""), data.get("tipo", "general")))
            objeto_id = cur.fetchone()[0]
        # Crear personaje genérico si no existe
        cur.execute("SELECT id FROM personaje WHERE nombre = %s", ("GENÉRICO",))
        row = cur.fetchone()
        if row:
            personaje_id = row[0]
        else:
            # Buscar una casa válida para el personaje genérico
            cur.execute("SELECT id FROM casa LIMIT 1")
            casa_row = cur.fetchone()
            casa_id = casa_row[0] if casa_row else None
            cur.execute("INSERT INTO personaje (nombre, fecha_nacimiento, alineacion, rol, casa_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", ("GENÉRICO", "1900-01-01", "neutro", "genérico", casa_id))
            personaje_id = cur.fetchone()[0]
        # Relacionar objeto con personaje
        cur.execute("INSERT INTO posee (personaje_id, objeto_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (personaje_id, objeto_id))
        # Buscar libro
        cur.execute("SELECT id FROM publicacion WHERE titulo = %s", (data["libro"],))
        libro_row = cur.fetchone()
        if not libro_row:
            print(f"[PostgreSQL] Libro '{data['libro']}' no encontrado")
            conn.rollback()
            cur.close()
            conn.close()
            return
        libro_id = libro_row[0]
        # Relacionar personaje con libro
        cur.execute("INSERT INTO aparece (personaje_id, publicacion_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (personaje_id, libro_id))
        conn.commit()
        print(f"[PostgreSQL] Objeto mágico '{data['nombre']}' asociado a libro '{data['libro']}' (vía personaje genérico)")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[PostgreSQL] Error al asociar objeto mágico: {e}")
def crear_personaje(data):
    """Crea un personaje y lo asocia a un libro en PostgreSQL"""
    import os
    from dotenv import load_dotenv
    import psycopg2
    # Cargar variables de entorno
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        print(f"[DEBUG] client_encoding: {conn.encoding}")
        cur = conn.cursor()
        # Buscar casa_id a partir del nombre de la casa (en mayúsculas)
        print(f"[DEBUG] Buscando casa: {data['casa']}")
        print(f"[DEBUG] Tipo de data['casa']: {type(data['casa'])}, valor: {data['casa']}")
        cur.execute("SELECT id FROM casa WHERE LOWER(nombre) = LOWER(%s)", (data["casa"],))
        casa_row = cur.fetchone()
        if not casa_row:
            print(f"[PostgreSQL] Casa '{data['casa']}' no encontrada")
            conn.rollback()
            cur.close()
            conn.close()
            return
        casa_id = casa_row[0]
        print(f"[DEBUG] casa_id encontrado: {casa_id}")
        # Verificar si el personaje ya existe
        print(f"[DEBUG] Tipo de data['nombre']: {type(data['nombre'])}, valor: {data['nombre']}")
        cur.execute("SELECT id FROM personaje WHERE nombre = %s", (data["nombre"],))
        if cur.fetchone():
            print(f"[PostgreSQL] Personaje '{data['nombre']}' ya existe, no se inserta de nuevo.")
        else:
            try:
                sql = """
                    INSERT INTO personaje (nombre, fecha_nacimiento, alineacion, rol, casa_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                valores = (
                    data["nombre"],
                    "1900-01-01",  # fecha_nacimiento por defecto
                    data["alineacion"],
                    data["rol"],
                    casa_id
                )
                print(f"[DEBUG] SQL: {sql.strip()}")
                print(f"[DEBUG] Valores: {valores}")
                for i, v in enumerate(valores):
                    print(f"[DEBUG] Valor {i}: tipo={type(v)}, valor={v}")
                cur.execute(sql, valores)
                print(f"[DEBUG] Personaje '{data['nombre']}' insertado")
                conn.commit()
            except Exception as insert_exc:
                print(f"[PostgreSQL] Error al insertar personaje: {insert_exc}")
        # Relacionar con libro
        print(f"[DEBUG] Tipo de data['libro']: {type(data['libro'])}, valor: {data['libro']}")
        cur.execute("SELECT id FROM publicacion WHERE titulo = %s", (data["libro"],))
        libro_row = cur.fetchone()
        if not libro_row:
            print(f"[PostgreSQL] Libro '{data['libro']}' no encontrado")
            conn.rollback()
            cur.close()
            conn.close()
            return
        libro_id = libro_row[0]
        cur.execute("SELECT id FROM personaje WHERE nombre = %s", (data["nombre"],))
        personaje_row = cur.fetchone()
        if not personaje_row:
            print(f"[PostgreSQL] No se pudo encontrar el personaje recién insertado")
            conn.rollback()
        personaje_id = personaje_row[0]
        cur.execute("""
            INSERT INTO aparece (personaje_id, publicacion_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (personaje_id, libro_id))
        conn.commit()
        try:
            print(f"[PostgreSQL] Personaje '{data['nombre']}' creado y asociado a libro '{data['libro']}'")
        except UnicodeEncodeError:
            print("[PostgreSQL] Personaje creado y asociado a libro (caracteres especiales en nombre/libro)")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[PostgreSQL] Error: {e}")

def crear_hechizo(data):
    print('[PostgreSQL] Crear hechizo:', data)

def crear_objeto_magico(data):
    print('[PostgreSQL] Crear objeto mágico:', data)

def crear_publicacion(data):
    print('[PostgreSQL] Crear publicación:', data)

def crear_criatura_magica(data):
    import os
    from dotenv import load_dotenv
    import psycopg2
    load_dotenv()
    DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
    DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DB_PORT = os.getenv('POSTGRES_PORT', 5433)
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()
        # Insertar criatura si no existe
        cur.execute("SELECT id FROM criaturamagica WHERE nombre = %s", (data["nombre"],))
        row = cur.fetchone()
        if row:
            criatura_id = row[0]
        else:
            cur.execute("INSERT INTO criaturamagica (nombre) VALUES (%s) RETURNING id", (data["nombre"],))
            criatura_id = cur.fetchone()[0]
        # Buscar libro
        cur.execute("SELECT id FROM publicacion WHERE titulo = %s", (data["libro"],))
        libro_row = cur.fetchone()
        if not libro_row:
            print(f"[PostgreSQL] Libro '{data['libro']}' no encontrado")
            conn.rollback()
            cur.close()
            conn.close()
            return
        libro_id = libro_row[0]
        # Asociar criatura al libro
        cur.execute("INSERT INTO mencion (criatura_id, publicacion_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (criatura_id, libro_id))
        conn.commit()
        print(f"[PostgreSQL] Monstruo '{data['nombre']}' creado y asociado a libro '{data['libro']}'")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[PostgreSQL] Error al crear monstruo: {e}")
