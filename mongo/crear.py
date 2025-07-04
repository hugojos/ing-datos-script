def crear_personaje(data):
    """Crea un personaje y lo asocia a un libro en MongoDB"""
    from db_mongo import get_db
    db = get_db()
    libro = db.libros.find_one({"titulo": data["libro"]})
    if not libro:
        print(f"[MongoDB] Libro '{data['libro']}' no encontrado")
        return
    personaje = {
        "nombre": data["nombre"],
        "rol": data["rol"],
        "casa": data["casa"],
        "alineacion": data["alineacion"]
    }
    db.libros.update_one({"_id": libro["_id"]}, {"$push": {"personajes": personaje}})
    print(f"[MongoDB] Personaje '{data['nombre']}' creado y asociado a libro '{data['libro']}'")

def crear_hechizo(data):
    print('[MongoDB] Crear hechizo:', data)

def crear_objeto_magico(data):
    print('[MongoDB] Crear objeto mágico:', data)

def crear_publicacion(data):
    print('[MongoDB] Crear publicación:', data)

def crear_criatura_magica(data):
    from db_mongo import get_db
    db = get_db()
    libro = db.libros.find_one({"titulo": data["libro"]})
    if not libro:
        print(f"[MongoDB] Libro '{data['libro']}' no encontrado")
        return
    criatura = {"nombre": data["nombre"]}
    # Asociar criatura al libro en el campo correcto que usa el caso de uso 3
    db.libros.update_one({"_id": libro["_id"]}, {"$push": {"criaturas": criatura}})
    print(f"[MongoDB] Monstruo '{data['nombre']}' creado y asociado a libro '{data['libro']}' (campo 'criaturas')")
