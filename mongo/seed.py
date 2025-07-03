import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_mongo import get_db




# Seed ajustado para reflejar exactamente las relaciones de las tablas Aparece, Posee y Mencion de PostgreSQL
libros = [
    {
        "titulo": "La Piedra Filosofal",
        "publicacion": 1997,
        "descripcion": "Primer libro",
        "personajes": [
            {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Hermione Granger", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Ron Weasley", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Albus Dumbledore", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Minerva McGonagall", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"}
        ],
        "criaturas": [],
        "objetoMagico": [
            {"nombre": "Varita de Saúco", "tipo": "varita", "descripcion": "La varita más poderosa", "duenio": "Harry Potter"},
            {"nombre": "Capa de Invisibilidad", "tipo": "capa", "descripcion": "Vuelve invisible", "duenio": "Harry Potter"}
        ]
    },
    {
        "titulo": "La Cámara Secreta",
        "publicacion": 1998,
        "descripcion": "Segundo libro",
        "personajes": [
            {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Hermione Granger", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Ron Weasley", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Albus Dumbledore", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Minerva McGonagall", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Severus Snape", "rol": "profesor", "casa": "Slytherin", "alineacion": "neutral"},
            {"nombre": "Draco Malfoy", "rol": "estudiante", "casa": "Slytherin", "alineacion": "neutral"}
        ],
        "criaturas": [ {"nombre": "Fawkes"} ],
        "objetoMagico": [
            {"nombre": "Varita de Harry", "tipo": "varita", "descripcion": "Varita de acebo", "duenio": "Harry Potter"},
            {"nombre": "Varita de Draco", "tipo": "varita", "descripcion": "Varita de espino", "1": "Draco Malfoy"},
            {"nombre": "Varita de Saúco", "tipo": "varita", "descripcion": "La varita más poderosa", "duenio": "Harry Potter"},
            {"nombre": "Varita de Draco", "tipo": "varita", "descripcion": "Varita de espino", "duenio": "Severus Snape"},
            {"nombre": "Capa de Invisibilidad", "tipo": "capa", "descripcion": "Vuelve invisible", "duenio": "Harry Potter"},
            {"nombre": "Giratiempos", "tipo": "objeto", "descripcion": "Permite viajar en el tiempo", "duenio": "Hermione Granger"}
        ]
    },
    {
        "titulo": "El Prisionero de Azkaban",
        "publicacion": 1999,
        "descripcion": "Tercer libro",
        "personajes": [
            {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Hermione Granger", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Ron Weasley", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Albus Dumbledore", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Minerva McGonagall", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Severus Snape", "rol": "profesor", "casa": "Slytherin", "alineacion": "neutral"},
            {"nombre": "Draco Malfoy", "rol": "estudiante", "casa": "Slytherin", "alineacion": "neutral"}
        ],
        "criaturas": [ {"nombre": "Buckbeak"} ],
        "objetoMagico": [
            {"nombre": "Varita de Harry", "tipo": "varita", "descripcion": "Varita de acebo", "duenio": "Harry Potter"},
            {"nombre": "Varita de Draco", "tipo": "varita", "descripcion": "Varita de espino", "duenio": "Draco Malfoy"},
            {"nombre": "Varita de Saúco", "tipo": "varita", "descripcion": "La varita más poderosa", "duenio": "Harry Potter"},
            {"nombre": "Varita de Draco", "tipo": "varita", "descripcion": "Varita de espino", "duenio": "Severus Snape"},
            {"nombre": "Capa de Invisibilidad", "tipo": "capa", "descripcion": "Vuelve invisible", "duenio": "Harry Potter"},
            {"nombre": "Giratiempos", "tipo": "objeto", "descripcion": "Permite viajar en el tiempo", "duenio": "Hermione Granger"}
        ]
    },
    {
        "titulo": "El Cáliz de Fuego",
        "publicacion": 2000,
        "descripcion": "Cuarto libro",
        "personajes": [
            {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Hermione Granger", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Ron Weasley", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Albus Dumbledore", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Minerva McGonagall", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Severus Snape", "rol": "profesor", "casa": "Slytherin", "alineacion": "neutral"},
            {"nombre": "Draco Malfoy", "rol": "estudiante", "casa": "Slytherin", "alineacion": "neutral"},
            {"nombre": "Voldemort", "rol": "villano", "casa": "Slytherin", "alineacion": "malo"}
        ],
        "criaturas": [ {"nombre": "Buckbeak"} ],
        "objetoMagico": [
            {"nombre": "Varita de Saúco", "tipo": "varita", "descripcion": "La varita más poderosa", "duenio": "Harry Potter"},
            {"nombre": "Capa de Invisibilidad", "tipo": "capa", "descripcion": "Vuelve invisible", "duenio": "Harry Potter"}
        ]
    },
    {
        "titulo": "La Orden del Fénix",
        "publicacion": 2003,
        "descripcion": "Quinto libro",
        "personajes": [
            {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Hermione Granger", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Ron Weasley", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Albus Dumbledore", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Minerva McGonagall", "rol": "profesor", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Severus Snape", "rol": "profesor", "casa": "Slytherin", "alineacion": "neutral"},
            {"nombre": "Draco Malfoy", "rol": "estudiante", "casa": "Slytherin", "alineacion": "neutral"},
            {"nombre": "Voldemort", "rol": "villano", "casa": "Slytherin", "alineacion": "malo"}
        ],
        "criaturas": [ {"nombre": "Fawkes"} ],
        "objetoMagico": [
            {"nombre": "Varita de Saúco", "tipo": "varita", "descripcion": "La varita más poderosa", "duenio": "Harry Potter"},
            {"nombre": "Capa de Invisibilidad", "tipo": "capa", "descripcion": "Vuelve invisible", "duenio": "Harry Potter"},
            {"nombre": "Giratiempos", "tipo": "objeto", "descripcion": "Permite viajar en el tiempo", "duenio": "Hermione Granger"}
        ]
    },
    {
        "titulo": "El Misterio del Príncipe",
        "publicacion": 2005,
        "descripcion": "Sexto libro",
        "personajes": [
            {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Severus Snape", "rol": "profesor", "casa": "Slytherin", "alineacion": "neutral"},
            {"nombre": "Voldemort", "rol": "villano", "casa": "Slytherin", "alineacion": "malo"}
        ],
        "criaturas": [],
        "objetoMagico": [
            {"nombre": "Horcrux", "tipo": "objeto", "descripcion": "Fragmento de alma", "duenio": "Voldemort"}
        ]
    },
    {
        "titulo": "Las Reliquias de la Muerte",
        "publicacion": 2007,
        "descripcion": "Último libro",
        "personajes": [
            {"nombre": "Harry Potter", "rol": "estudiante", "casa": "Gryffindor", "alineacion": "bueno"},
            {"nombre": "Voldemort", "rol": "villano", "casa": "Slytherin", "alineacion": "malo"}
        ],
        "criaturas": [ {"nombre": "Nagini"} ],
        "objetoMagico": [
            {"nombre": "Horcrux", "tipo": "objeto", "descripcion": "Fragmento de alma", "duenio": "Voldemort"}
        ]
    }
]

def seed_libros():
    db = get_db()
    db.libros.delete_many({})
    db.libros.insert_many(libros)
    print("Colección 'libros' poblada correctamente.")

if __name__ == "__main__":
    seed_libros()
