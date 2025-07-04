import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_neo4j import get_neo4j_connection, limpiar_base_datos, crear_indices, obtener_estadisticas
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

def reset_neo4j():
    """Resetea completamente la base de datos Neo4j"""
    console.print(Panel("[bold blue]Iniciando reset de Neo4j[/bold blue]", title="Neo4j Reset"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        
        # Paso 1: Probar conexión
        task = progress.add_task("Probando conexión con Neo4j...", total=None)
        try:
            neo4j_conn = get_neo4j_connection()
            if not neo4j_conn.connect():
                console.print("[bold red]❌ No se pudo conectar a Neo4j[/bold red]")
                console.print("[yellow]Asegúrate de que el contenedor de Neo4j esté ejecutándose:[/yellow]")
                console.print("[dim]docker-compose up -d neo4j[/dim]")
                return False
            neo4j_conn.close()
            progress.update(task, description="✅ Conexión exitosa")
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]❌ Error al conectar: {e}[/bold red]")
            return False
        
        # Paso 2: Obtener estadísticas antes del reset
        progress.update(task, description="Obteniendo estadísticas previas...")
        console.print("\n[bold yellow]Estadísticas antes del reset:[/bold yellow]")
        obtener_estadisticas()
        time.sleep(1)
        
        # Paso 3: Limpiar base de datos
        progress.update(task, description="Limpiando base de datos...")
        try:
            limpiar_base_datos()
            progress.update(task, description="✅ Base de datos limpiada")
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]❌ Error al limpiar base de datos: {e}[/bold red]")
            return False
        
        # Paso 4: Crear índices
        progress.update(task, description="Creando índices...")
        try:
            crear_indices()
            progress.update(task, description="✅ Índices creados")
            time.sleep(0.5)
        except Exception as e:
            console.print(f"[bold red]❌ Error al crear índices: {e}[/bold red]")
            return False
        
        # Paso 5: Verificar estado final
        progress.update(task, description="Verificando estado final...")
        console.print("\n[bold green]Estadísticas después del reset:[/bold green]")
        obtener_estadisticas()
        progress.update(task, description="✅ Reset completado")
    
    console.print(Panel("[bold green]✅ Reset de Neo4j completado exitosamente[/bold green]", title="Éxito"))
    console.print("\n[bold cyan]Base de datos Neo4j lista para usar:[/bold cyan]")
    console.print("• Todos los nodos y relaciones eliminados")
    console.print("• Índices recreados para optimizar consultas")
    console.print("• Conexión verificada y funcionando")
    
    return True

def crear_estructura_base():
    """Crea la estructura básica de la base de datos con algunos datos de ejemplo"""
    console.print(Panel("[bold blue]Creando estructura básica[/bold blue]", title="Estructura Base"))
    
    try:
        neo4j_conn = get_neo4j_connection()
        if neo4j_conn.connect():
            # Crear algunos nodos de ejemplo para verificar que todo funciona
            consultas_ejemplo = [
                """
                CREATE (h:Hechizo {
                    nombre: 'Expelliarmus',
                    descripcion: 'Desarmador',
                    dificultad: 'Intermedio',
                    tipo: 'Defensivo'
                })
                """,
                """
                CREATE (p:Personaje {
                    nombre: 'Harry Potter',
                    casa: 'Gryffindor',
                    sangre: 'Mestiza',
                    ocupacion: 'Estudiante'
                })
                """,
                """
                CREATE (o:ObjetoMagico {
                    nombre: 'Varita de Saúco',
                    descripcion: 'La varita más poderosa que existe',
                    rareza: 'Única',
                    origen: 'Desconocido'
                })
                """
            ]
            
            for consulta in consultas_ejemplo:
                neo4j_conn.execute_query(consulta)
            
            console.print("[bold green]✅ Estructura básica creada con datos de ejemplo[/bold green]")
        neo4j_conn.close()
    except Exception as e:
        console.print(f"[bold red]❌ Error al crear estructura base: {e}[/bold red]")

def main():
    """Función principal que ejecuta el reset completo"""
    console.print("[bold magenta]🔄 Iniciando proceso de reset de Neo4j...[/bold magenta]")
    
    # Resetear la base de datos
    if reset_neo4j():
        # Preguntar si crear estructura básica
        console.print("\n[bold yellow]¿Deseas crear una estructura básica con datos de ejemplo? (y/n):[/bold yellow]", end=" ")
        respuesta = input().strip().lower()
        
        if respuesta in ['y', 'yes', 'sí', 's']:
            crear_estructura_base()
            console.print("\n[bold green]Estado final:[/bold green]")
            obtener_estadisticas()
    else:
        console.print("[bold red]❌ El proceso de reset falló[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
