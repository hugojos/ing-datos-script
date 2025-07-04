
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()

# Cargar variables de entorno
load_dotenv()

DB_NAME = os.getenv('POSTGRES_DB', 'harry_potter')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', 5433)

CREATE_TABLES_SQL = '''
-- Tabla Casa
CREATE TABLE Casa (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fundador VARCHAR(100),
    valores TEXT,
    mascota VARCHAR(100)
);

-- Tabla Personaje
CREATE TABLE Personaje (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    alineacion VARCHAR(50),
    rol VARCHAR(100),
    casa_id INTEGER REFERENCES Casa(id)
);

-- Tabla Hechizo
CREATE TABLE Hechizo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    efecto TEXT
);

-- Tabla ObjetoMagico
CREATE TABLE ObjetoMagico (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50)
);

-- Tabla Evento
CREATE TABLE Evento (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha DATE
);

-- Tabla Publicacion
CREATE TABLE Publicacion (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50),
    ano_lanzamiento INT
);

-- Tabla CriaturaMagica
CREATE TABLE CriaturaMagica (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Relación: Personaje aprende o usa un hechizo
CREATE TABLE Aprende (
    personaje_id INTEGER REFERENCES Personaje(id),
    hechizo_id INTEGER REFERENCES Hechizo(id),
    veces_usado INT DEFAULT 1,
    PRIMARY KEY (personaje_id, hechizo_id)
);

-- Relación: Personaje posee un objeto mágico
CREATE TABLE Posee (
    personaje_id INTEGER REFERENCES Personaje(id),
    objeto_id INTEGER REFERENCES ObjetoMagico(id),
    PRIMARY KEY (personaje_id, objeto_id)
);

-- Relación: Personaje aparece en una publicación
CREATE TABLE Aparece (
    personaje_id INTEGER REFERENCES Personaje(id),
    publicacion_id INTEGER REFERENCES Publicacion(id),
    PRIMARY KEY (personaje_id, publicacion_id)
);

-- Relación: Criatura mágica mencionada en una publicación
CREATE TABLE Mencion (
    criatura_id INTEGER REFERENCES CriaturaMagica(id),
    publicacion_id INTEGER REFERENCES Publicacion(id),
    PRIMARY KEY (criatura_id, publicacion_id)
);

-- Relación: Personaje participa en un evento
CREATE TABLE Participa (
    personaje_id INTEGER REFERENCES Personaje(id),
    evento_id INTEGER REFERENCES Evento(id),
    PRIMARY KEY (personaje_id, evento_id)
);

-- Relación: Evento ocurre en una publicación
CREATE TABLE Ocurre (
    evento_id INTEGER REFERENCES Evento(id),
    publicacion_id INTEGER REFERENCES Publicacion(id),
    PRIMARY KEY (evento_id, publicacion_id)
);
'''

def reset_database():
    # Conectar a la base postgres para poder dropear la base objetivo
    conn = psycopg2.connect(dbname='postgres', user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    # Terminar conexiones activas
    cur.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{DB_NAME}';")
    # Drop y create
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
    cur.execute(f"CREATE DATABASE {DB_NAME} WITH ENCODING 'UTF8' LC_COLLATE='C.UTF-8' LC_CTYPE='C.UTF-8' TEMPLATE=template0;")
    cur.close()
    conn.close()
    console.print(Panel(f"[bold green]Base de datos '{DB_NAME}' reseteada.[/bold green]", title="PostgreSQL Reset"))

    # Conectar a la base recién creada y crear tablas
    conn2 = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur2 = conn2.cursor()
    for statement in CREATE_TABLES_SQL.split(';'):
        stmt = statement.strip()
        if stmt:
            cur2.execute(stmt+';')
    conn2.commit()
    cur2.close()
    conn2.close()
    console.print(Panel("[bold green]Tablas creadas correctamente.[/bold green]", title="PostgreSQL Reset"))
    # Ejecutar seed.py automáticamente
    import subprocess
    try:
        subprocess.run(["py", "postgresql/seed.py"], check=True)
        console.print(Panel("[bold green]Datos de ejemplo insertados correctamente (seed.py ejecutado).[/bold green]", title="PostgreSQL Seed"))
    except Exception as e:
        console.print(Panel(f"[bold red]No se pudo ejecutar seed.py automáticamente: {e}[/bold red]", title="Error"))

if __name__ == "__main__":
    reset_database()
