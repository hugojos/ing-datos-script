def crear_personaje(data):
    """Crea un personaje y lo asocia a un libro en PostgreSQL"""
    import psycopg2
    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432
        )
        # Forzar encoding UTF-8 en la conexión
        conn.set_client_encoding('UTF8')
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
                    ON CONFLICT (nombre) DO NOTHING
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
    print('[PostgreSQL] Crear criatura mágica:', data)
