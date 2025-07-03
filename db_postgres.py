import os
import psycopg2
from psycopg2 import sql

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def get_postgres_connection():
    os.environ['PGCLIENTENCODING'] = 'UTF8'
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', 5432),
        dbname=os.getenv('POSTGRES_DB', 'harry_potter'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', ''),
        client_encoding='UTF8'
    )
    conn.set_client_encoding('UTF8')
    return conn


def test_postgres_connection():
    try:
        conn = get_postgres_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        print("Conexión exitosa a PostgreSQL. Versión:")
        try:
            print(str(version[0]))
        except UnicodeDecodeError:
            print("(No se pudo mostrar la versión por un problema de codificación, pero la conexión es exitosa.)")
        except Exception as e:
            print(f"(Error inesperado al mostrar la versión: {e})")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")

def crear_tabla_personaje():
    try:
        conn = get_postgres_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS personaje (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                casa VARCHAR(50),
                es_mago BOOLEAN
            );
        ''')
        conn.commit()
        print("Tabla 'personaje' creada o ya existente.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al crear la tabla personaje: {e}")

def insertar_personaje(nombre, casa, es_mago):
    try:
        conn = get_postgres_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO personaje (nombre, casa, es_mago) VALUES (%s, %s, %s) RETURNING id;
        ''', (nombre, casa, es_mago))
        personaje_id = cur.fetchone()[0]
        conn.commit()
        print(f"Personaje insertado con id: {personaje_id}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al insertar personaje: {e}")

def mostrar_personajes():
    try:
        conn = get_postgres_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, nombre, casa, es_mago FROM personaje;')
        rows = cur.fetchall()
        print("\nListado de personajes en la base de datos:")
        for row in rows:
            try:
                print(row)
            except UnicodeDecodeError:
                print("(No se pudo mostrar un registro por un problema de codificación.)")
            except Exception as e:
                print(f"(Error inesperado al mostrar un registro: {e})")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al mostrar personajes: {e}")

if __name__ == "__main__":
    test_postgres_connection()
    crear_tabla_personaje()
    insertar_personaje("Harry Potter", "Gryffindor", True)
    mostrar_personajes()
