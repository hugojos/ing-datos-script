import sys
import os
import time
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_mongo import get_db

console = Console()

def caso_1():
    db = get_db()
    start = time.perf_counter()
    cursor = db.libros.find({}, {
        '_id': 0,
        'titulo': 1,
        'cantidad_personajes': {'$size': "$personajes"}
    })
    elapsed = (time.perf_counter() - start) * 1000
    table = Table(title="Personajes por libro (MongoDB)")
    table.add_column("Libro", style="cyan")
    table.add_column("Cantidad de personajes", style="magenta")
    for doc in cursor:
        table.add_row(str(doc.get('titulo', '')), str(doc.get('cantidad_personajes', '')))
    console.print(table)
    console.print(f"[green]Consulta MongoDB ejecutada en {elapsed:.2f} ms[/green]")

def caso_2():
    db = get_db()
    start = time.perf_counter()
    pipeline = [
        { '$unwind': "$objetoMagico" },
        { '$group': { '_id': "$objetoMagico.nombre", 'apariciones': { '$sum': 1 } } },
        { '$sort': { 'apariciones': -1 } }
    ]
    cursor = db.libros.aggregate(pipeline)
    elapsed = (time.perf_counter() - start) * 1000
    table = Table(title="Apariciones de objetos mágicos (MongoDB)")
    table.add_column("Objeto Mágico", style="cyan")
    table.add_column("Apariciones", style="magenta")
    for doc in cursor:
        table.add_row(str(doc.get('_id', '')), str(doc.get('apariciones', '')))
    console.print(table)
    console.print(f"[green]Consulta MongoDB ejecutada en {elapsed:.2f} ms[/green]")

def caso_3():
    db = get_db()
    start = time.perf_counter()
    cursor = db.libros.find({}, {
        '_id': 0,
        'titulo': 1,
        'criaturas': 1
    })
    elapsed = (time.perf_counter() - start) * 1000
    table = Table(title="Criaturas por libro (MongoDB)")
    table.add_column("Libro", style="cyan")
    table.add_column("Criaturas", style="magenta")
    for doc in cursor:
        criaturas = ', '.join([c.get('nombre', '') for c in doc.get('criaturas', [])]) if doc.get('criaturas') else '-'
        table.add_row(str(doc.get('titulo', '')), criaturas)
    console.print(table)
    console.print(f"[green]Consulta MongoDB ejecutada en {elapsed:.2f} ms[/green]")

def caso_4():
    db = get_db()
    start = time.perf_counter()
    pipeline = [
        { '$unwind': "$personajes" },
        { '$match': { "personajes.rol": "profesor" } },
        { '$group': {
            '_id': "$personajes.nombre",
            'cantidad_libros': { '$sum': 1 }
        }},
        { '$match': { 'cantidad_libros': { '$gt': 4 } } }
    ]
    cursor = db.libros.aggregate(pipeline)
    elapsed = (time.perf_counter() - start) * 1000
    table = Table(title="Profesores que aparecen en más de 4 libros (MongoDB)")
    table.add_column("Profesor", style="cyan")
    table.add_column("Cantidad de libros", style="magenta")
    for doc in cursor:
        table.add_row(str(doc.get('_id', '')), str(doc.get('cantidad_libros', '')))
    console.print(table)
    console.print(f"[green]Consulta MongoDB ejecutada en {elapsed:.2f} ms[/green]")

def caso_5():
    db = get_db()
    start = time.perf_counter()
    pipeline = [
        {
            '$facet': {
                'objetosDelUltimoLibro': [
                    { '$match': { 'titulo': "Las Reliquias de la Muerte" } },
                    { '$unwind': "$objetoMagico" },
                    { '$replaceRoot': { 'newRoot': "$objetoMagico" } }
                ],
                'objetosDePersonajesBuenos': [
                    { '$unwind': "$personajes" },
                    { '$match': { 'personajes.alineacion': "bueno" } },
                    { '$group': { '_id': None, 'nombresBuenos': { '$addToSet': "$personajes.nombre" } } },
                    {
                        '$lookup': {
                            'from': "libros",
                            'pipeline': [
                                { '$unwind': "$objetoMagico" },
                                { '$replaceRoot': { 'newRoot': "$objetoMagico" } }
                            ],
                            'as': "todosObjetos"
                        }
                    },
                    { '$unwind': "$todosObjetos" },
                    { '$match': { '$expr': { '$in': ["$todosObjetos.duenio", "$nombresBuenos"] } } },
                    { '$replaceRoot': { 'newRoot': "$todosObjetos" } }
                ]
            }
        },
        { '$project': { 'objetosUnicos': { '$setUnion': ["$objetosDelUltimoLibro", "$objetosDePersonajesBuenos"] } } },
        { '$project': { 'cantidad': { '$size': "$objetosUnicos" } } }
    ]
    cursor = db.libros.aggregate(pipeline)
    elapsed = (time.perf_counter() - start) * 1000
    cantidad = 0
    for doc in cursor:
        cantidad = doc.get('cantidad', 0)
    table = Table(title="Cantidad de objetos mágicos únicos (MongoDB)")
    table.add_column("Cantidad", style="magenta")
    table.add_row(str(cantidad))
    console.print(table)
    console.print(f"[green]Consulta MongoDB ejecutada en {elapsed:.2f} ms[/green]")

def caso_6():
    db = get_db()
    start = time.perf_counter()
    pipeline = [
        { '$unwind': "$objetoMagico" },
        { '$match': { 'objetoMagico.nombre': { '$regex': "varita", '$options': "i" } } },
        { '$group': {
            '_id': "$objetoMagico.nombre",
            'duenios': { '$addToSet': "$objetoMagico.duenio" },
            'hechizos': { '$push': "$objetoMagico.hechizosLanzados" }
        }},
        { '$project': {
            'cantidadDuenios': { '$size': "$duenios" },
            'hechizos': {
                '$reduce': {
                    'input': "$hechizos",
                    'initialValue': [],
                    'in': { '$concatArrays': ["$$value", "$$this"] }
                }
            }
        }},
        { '$sort': { 'cantidadDuenios': -1 } },
        { '$limit': 1 },
        { '$unwind': "$hechizos" },
        { '$group': {
            '_id': { 'hechizo': "$hechizos.nombre" },
            'cantidadUsos': { '$sum': 1 }
        }},
        { '$sort': { 'cantidadUsos': -1 } },
        { '$limit': 1 },
        { '$project': {
            'hechizoMasUsado': "$_id.hechizo",
            'cantidadUsos': 1,
            '_id': 0
        }}
    ]
    cursor = db.libros.aggregate(pipeline)
    elapsed = (time.perf_counter() - start) * 1000
    hechizo = None
    cantidad = 0
    for doc in cursor:
        hechizo = doc.get('hechizoMasUsado', '-')
        cantidad = doc.get('cantidadUsos', 0)
    table = Table(title="Hechizo más usado por varitas (MongoDB)")
    table.add_column("Hechizo", style="cyan")
    table.add_column("Cantidad de usos", style="magenta")
    table.add_row(str(hechizo), str(cantidad))
    console.print(table)
    console.print(f"[green]Consulta MongoDB ejecutada en {elapsed:.2f} ms[/green]")
