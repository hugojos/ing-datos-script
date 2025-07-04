
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Importar funciones de creación
from mongo.crear import crear_personaje as crear_personaje_mongo, crear_hechizo as crear_hechizo_mongo, crear_objeto_magico as crear_objeto_magico_mongo, crear_publicacion as crear_publicacion_mongo, crear_criatura_magica as crear_criatura_magica_mongo
from postgresql.crear import crear_personaje as crear_personaje_postgres, crear_hechizo as crear_hechizo_postgres, crear_objeto_magico as crear_objeto_magico_postgres, crear_publicacion as crear_publicacion_postgres, crear_criatura_magica as crear_criatura_magica_postgres

# Importar funciones de casos de uso
from mongo.caso_de_uso import caso_1 as caso_1_mongo, caso_2 as caso_2_mongo, caso_3 as caso_3_mongo, caso_4 as caso_4_mongo, caso_5 as caso_5_mongo, caso_6 as caso_6_mongo
from postgresql.caso_de_uso import caso_1 as caso_1_postgres, caso_2 as caso_2_postgres, caso_3 as caso_3_postgres, caso_4 as caso_4_postgres, caso_5 as caso_5_postgres, caso_6 as caso_6_postgres
from neo4j_app.caso_de_uso import caso_1 as caso_1_neo4j, caso_2 as caso_2_neo4j, caso_3 as caso_3_neo4j, caso_4 as caso_4_neo4j, caso_5 as caso_5_neo4j, caso_6 as caso_6_neo4j

console = Console()

def mostrar_menu():
    """Muestra el menú principal con las opciones disponibles usando rich."""
    menu_text = Text("\n         MENÚ PRINCIPAL\n", style="bold magenta")
    menu_text.append("\n[9] Reiniciar DBs\n", style="bold yellow")
    menu_text.append("[1] Crear\n", style="bold cyan")
    menu_text.append("[2] Casos de uso\n", style="bold cyan")
    menu_text.append("[0] Salir\n", style="bold red")
    console.print(Panel(menu_text, title="[bold yellow]Menú[/bold yellow]", border_style="bright_blue", expand=False))

def obtener_opcion():
    """Obtiene y valida la opción seleccionada por el usuario."""
    while True:
        opcion = console.input("[bold green]\nSelecciona una opción (9, 1-2, 0 para salir): [/bold green]").strip()
        if opcion in ('9', '1', '2', '0'):
            return opcion
        console.print("[bold red]❌ Opción inválida. Por favor, selecciona 9, 1, 2 o 0.[/bold red]")
import subprocess

def reiniciar_dbs():
    console.print("\n[bold yellow]Reiniciando bases de datos...[/bold yellow]")
    # PostgreSQL
    try:
        subprocess.run(["py", "postgresql/reset.py"], check=True)
        console.print("[bold green]PostgreSQL reiniciada correctamente.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error al reiniciar PostgreSQL: {e}[/bold red]")
    # MongoDB
    try:
        subprocess.run(["py", "mongo/reset.py"], check=True)
        console.print("[bold green]MongoDB reiniciada correctamente.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error al reiniciar MongoDB: {e}[/bold red]")
    # Neo4j (reset y seed)
    try:
        subprocess.run(["py", "neo4j_app/crear.py"], check=True)
        console.print("[bold green]Neo4j reiniciada correctamente.[/bold green]")
        subprocess.run(["py", "neo4j_app/seed.py"], check=True)
        console.print("[bold green]Neo4j poblada con datos de ejemplo.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error al reiniciar o poblar Neo4j: {e}[/bold red]")
    console.input("\n[bold green]Presiona Enter para continuar...[/bold green]")

def opcion_crear():
    while True:
        console.print("\n[bold yellow]🔧 Has seleccionado: CREAR[/bold yellow]")
        crear_text = Text("\n¿Qué deseas crear?\n", style="bold yellow")
        crear_text.append("1. Personaje\n", style="bold cyan")
        crear_text.append("2. Hechizo\n", style="bold cyan")
        crear_text.append("3. Objeto Mágico\n", style="bold cyan")
        crear_text.append("4. Publicación\n", style="bold cyan")
        crear_text.append("5. Criatura Mágica\n", style="bold cyan")
        crear_text.append("0. Volver al menú principal\n", style="bold red")
        console.print(Panel(crear_text, title="[bold yellow]Crear[/bold yellow]", border_style="bright_blue", expand=False))
        opcion = console.input("[bold green]\nSelecciona una opción (1-5, 0 para volver): [/bold green]").strip()
        if opcion == '0':
            break
        elif opcion == '1':
            data = {"nombre": "Ejemplo Personaje"}
            crear_personaje_mongo(data)
            crear_personaje_postgres(data)
            console.print("\n[bold blue][1] Personaje creado en las 3 bases de datos[/bold blue]")
        elif opcion == '2':
            data = {"nombre": "Ejemplo Hechizo"}
            crear_hechizo_mongo(data)
            crear_hechizo_postgres(data)
            console.print("\n[bold blue][2] Hechizo creado en las 3 bases de datos[/bold blue]")
        elif opcion == '3':
            data = {"nombre": "Ejemplo Objeto Mágico"}
            crear_objeto_magico_mongo(data)
            crear_objeto_magico_postgres(data)
            console.print("\n[bold blue][3] Objeto Mágico creado en las 3 bases de datos[/bold blue]")
        elif opcion == '4':
            data = {"nombre": "Ejemplo Publicación"}
            crear_publicacion_mongo(data)
            crear_publicacion_postgres(data)
            console.print("\n[bold blue][4] Publicación creada en las 3 bases de datos[/bold blue]")
        elif opcion == '5':
            data = {"nombre": "Ejemplo Criatura Mágica"}
            crear_criatura_magica_mongo(data)
            crear_criatura_magica_postgres(data)
            console.print("\n[bold blue][5] Criatura Mágica creada en las 3 bases de datos[/bold blue]")
        else:
            console.print("[bold red]❌ Opción inválida. Por favor, selecciona una opción válida.[/bold red]")
        console.input("\n[bold green]Presiona Enter para continuar...[/bold green]")

def opcion_casos_uso():
    while True:
        console.print("\n[bold magenta]📋 Has seleccionado: CASOS DE USO[/bold magenta]")
        casos_text = Text("\nCasos de Uso\n", style="bold yellow")
        casos_text.append("1. ¿Cuántos personajes aparecen en cada libro de la serie?\n", style="bold cyan")
        casos_text.append("2. ¿Qué objetos mágicos tienen más relevancia en la trama de la saga? (aparecen más veces)\n", style="bold cyan")
        casos_text.append("3. ¿Qué criaturas mágicas aparecen en cada libro?\n", style="bold cyan")
        casos_text.append("4. ¿Qué personajes han aparecido en más de 4 libros Y tienen un rol de profesor?\n", style="bold cyan")
        casos_text.append("5. ¿Cuántos objetos mágicos son mencionados en el último libro O pertenecen a un personaje bueno de todos los libros?\n", style="bold cyan")
        casos_text.append("6. ¿Cuál ha sido la varita que ha pasado por más personajes y cuál ha sido el hechizo más usado por ese personaje con esa varita?\n", style="bold cyan")
        casos_text.append("0. Volver al menú principal\n", style="bold red")
        console.print(Panel(casos_text, title="[bold yellow]Casos de Uso[/bold yellow]", border_style="bright_blue", expand=False))
        opcion = console.input("[bold green]\nSelecciona una opción (1-6, 0 para volver): [/bold green]").strip()
        if opcion == '0':
            break
        elif opcion == '1':
            console.rule("[bold blue]PostgreSQL[/bold blue]")
            caso_1_postgres()
            console.rule("[bold green]MongoDB[/bold green]")
            caso_1_mongo()
            console.rule("[bold magenta]Neo4j[/bold magenta]")
            caso_1_neo4j()
        elif opcion == '2':
            console.rule("[bold blue]PostgreSQL[/bold blue]")
            caso_2_postgres()
            console.rule("[bold green]MongoDB[/bold green]")
            caso_2_mongo()
            console.rule("[bold magenta]Neo4j[/bold magenta]")
            caso_2_neo4j()
        elif opcion == '3':
            console.rule("[bold blue]PostgreSQL[/bold blue]")
            caso_3_postgres()
            console.rule("[bold green]MongoDB[/bold green]")
            caso_3_mongo()
            console.rule("[bold magenta]Neo4j[/bold magenta]")
            caso_3_neo4j()
        elif opcion == '4':
            console.rule("[bold blue]PostgreSQL[/bold blue]")
            caso_4_postgres()
            console.rule("[bold green]MongoDB[/bold green]")
            caso_4_mongo()
            console.rule("[bold magenta]Neo4j[/bold magenta]")
            caso_4_neo4j()
        elif opcion == '5':
            console.rule("[bold blue]PostgreSQL[/bold blue]")
            caso_5_postgres()
            console.rule("[bold green]MongoDB[/bold green]")
            caso_5_mongo()
            console.rule("[bold magenta]Neo4j[/bold magenta]")
            caso_5_neo4j()
        elif opcion == '6':
            console.rule("[bold blue]PostgreSQL[/bold blue]")
            caso_6_postgres()
            console.rule("[bold green]MongoDB[/bold green]")
            caso_6_mongo()
            console.rule("[bold magenta]Neo4j[/bold magenta]")
            caso_6_neo4j()
        else:
            console.print("[bold red]❌ Opción inválida. Por favor, selecciona una opción válida.[/bold red]")
            continue
        console.input("\n[bold green]Presiona Enter para continuar...[/bold green]")

def main():
    console.print("[bold green]🚀 Bienvenido al menú GPT-4.1[/bold green]")
    while True:
        mostrar_menu()
        opcion = obtener_opcion()
        if opcion == '9':
            reiniciar_dbs()
        elif opcion == '1':
            opcion_crear()
        elif opcion == '2':
            opcion_casos_uso()
        elif opcion == '0':
            console.print("\n[bold magenta]👋 ¡Hasta luego![/bold magenta]")
            break

if __name__ == "__main__":
    main()
