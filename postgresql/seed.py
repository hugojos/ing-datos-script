
import os
import psycopg2
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

def seed():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    # Limpiar tablas
    cur.execute('''
        DELETE FROM Ocurre;
        DELETE FROM Participa;
        DELETE FROM Mencion;
        DELETE FROM Aparece;
        DELETE FROM Posee;
        DELETE FROM Aprende;
        DELETE FROM CriaturaMagica;
        DELETE FROM Publicacion;
        DELETE FROM Evento;
        DELETE FROM ObjetoMagico;
        DELETE FROM Hechizo;
        DELETE FROM Personaje;
        DELETE FROM Casa;
    ''')
    # Casas
    cur.execute("""
        INSERT INTO Casa (id, nombre, fundador, valores, mascota) VALUES
          (1, 'Gryffindor', 'Godric Gryffindor', 'Valor, coraje', 'León'),
          (2, 'Slytherin', 'Salazar Slytherin', 'Astucia, ambición', 'Serpiente');
    """)
    # Publicaciones (libros)
    cur.execute("""
        INSERT INTO Publicacion (id, titulo, descripcion, tipo, ano_lanzamiento) VALUES
          (1, 'La Piedra Filosofal', 'Primer libro', 'libro', 1997),
          (2, 'La Cámara Secreta', 'Segundo libro', 'libro', 1998),
          (3, 'El Prisionero de Azkaban', 'Tercer libro', 'libro', 1999),
          (4, 'El Cáliz de Fuego', 'Cuarto libro', 'libro', 2000),
          (5, 'La Orden del Fénix', 'Quinto libro', 'libro', 2003),
          (6, 'El Misterio del Príncipe', 'Sexto libro', 'libro', 2005),
          (7, 'Las Reliquias de la Muerte', 'Último libro', 'libro', 2007);
    """)
    # Personajes
    cur.execute("""
        INSERT INTO Personaje (id, nombre, fecha_nacimiento, alineacion, rol, casa_id) VALUES
          (1, 'Harry Potter', '1980-07-31', 'bueno', 'estudiante', 1),
          (2, 'Hermione Granger', '1979-09-19', 'bueno', 'estudiante', 1),
          (3, 'Ron Weasley', '1980-03-01', 'bueno', 'estudiante', 1),
          (4, 'Albus Dumbledore', '1881-08-01', 'bueno', 'profesor', 1),
          (5, 'Severus Snape', '1960-01-09', 'neutral', 'profesor', 2),
          (6, 'Draco Malfoy', '1980-06-05', 'neutral', 'estudiante', 2),
          (7, 'Minerva McGonagall', '1935-10-04', 'bueno', 'profesor', 1),
          (8, 'Voldemort', '1926-12-31', 'malo', 'villano', 2);
    """)
    # Hechizos
    cur.execute("""
        INSERT INTO Hechizo (id, nombre, descripcion, efecto) VALUES
          (1, 'Expelliarmus', 'Desarma al oponente', 'Desarme'),
          (2, 'Avada Kedavra', 'Mata instantáneamente', 'Mortal'),
          (3, 'Expecto Patronum', 'Invoca un patronus', 'Defensa'),
          (4, 'Wingardium Leviosa', 'Levita objetos', 'Levitación');
    """)
    # Objetos mágicos (incluyendo varitas)
    cur.execute("""
        INSERT INTO ObjetoMagico (id, nombre, descripcion, tipo) VALUES
          (1, 'Varita de Saúco', 'La varita más poderosa', 'varita'),
          (2, 'Varita de Harry', 'Varita de acebo', 'varita'),
          (3, 'Varita de Draco', 'Varita de espino', 'varita'),
          (4, 'Capa de Invisibilidad', 'Vuelve invisible', 'capa'),
          (5, 'Horcrux', 'Fragmento de alma', 'objeto'),
          (6, 'Giratiempos', 'Permite viajar en el tiempo', 'objeto');
    """)
    # Criaturas mágicas
    cur.execute("""
        INSERT INTO CriaturaMagica (id, nombre) VALUES
          (1, 'Buckbeak'),
          (2, 'Fawkes'),
          (3, 'Nagini');
    """)
    # Eventos
    cur.execute("""
        INSERT INTO Evento (id, nombre, descripcion, fecha) VALUES
          (1, 'Torneo de los Tres Magos', 'Competencia mágica', '1994-06-24'),
          (2, 'Batalla de Hogwarts', 'Batalla final', '1998-05-02');
    """)
    # Relaciones: Aparece (personaje en libro)
    cur.execute("""
        INSERT INTO Aparece (personaje_id, publicacion_id) VALUES
          (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
          (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
          (3,1),(3,2),(3,3),(3,4),(3,5),
          (4,1),(4,2),(4,3),(4,4),(4,5),
          (5,2),(5,3),(5,4),(5,5),
          (6,2),(6,3),(6,4),(6,5),
          (7,1),(7,2),(7,3),(7,4),(7,5),
          (8,4),(8,5),(8,6),(8,7);
    """)
    # Relaciones: Posee (personaje-objeto)
    cur.execute("""
        INSERT INTO Posee (personaje_id, objeto_id) VALUES
          (1,1),(1,4),
          (2,6),
          (3,2),
          (4,1),
          (5,3),
          (6,3),
          (8,5);
    """)
    # Relaciones: Aprende (personaje-hechizo)
    cur.execute("""
        INSERT INTO Aprende (personaje_id, hechizo_id, veces_usado) VALUES
          (1,1,10),
          (2,4,7),
          (4,3,8),
          (5,2,4),
          (6,1,2),
          (7,3,3);
    """)
    # Relaciones: Mencion (criatura-libro)
    cur.execute("""
        INSERT INTO Mencion (criatura_id, publicacion_id) VALUES
          (1,3), (1,4), (2,2), (2,5), (3,7);
    """)
    # Relaciones: Participa (personaje-evento)
    cur.execute("""
        INSERT INTO Participa (personaje_id, evento_id) VALUES
          (1,1),(1,2),
          (2,1),
          (4,1),(4,2),
          (8,2);
    """)
    # Relaciones: Ocurre (evento-libro)
    cur.execute("""
        INSERT INTO Ocurre (evento_id, publicacion_id) VALUES
          (1,4), (2,7);
    """)
    conn.commit()
    cur.close()
    conn.close()
    console.print(Panel("[bold green]Seed ejecutado correctamente.[/bold green]", title="PostgreSQL Seed"))

if __name__ == "__main__":
    seed()
