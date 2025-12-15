import subprocess, sys, os
from PicSortType import organize_photos_by_type
from PictDuplicateFinder import find_and_remove_duplicates
from analyze_photos import analyze_directory, print_report
from delete_duplicates import delete_all_duplicates

# Rutas base (puedes modificarlas aquí)
SOURCE_DIR = r"/Users/RobertoAbad/Pictures"
OUTPUT_DIR = r"/Users/RobertoAbad/Pictures/formats/Duplicados_detectados"
BACKUP_DIR = r"/Users/RobertoAbad/Pictures/formats/Duplicados_Eliminados"
PICTURES_DIR = "/Users/RobertoAbad/Pictures"
DUPLICATES_DIR = os.path.join(PICTURES_DIR, "formats", "Duplicados_Eliminados")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_console()
        print("=" * 50)
        print("""
==================================================
📸 PHOTO ORGANIZER MENU
==================================================
1. Organizar fotos por tipo (RAW, JPG, PNG, etc.)
2. Detectar y limpiar duplicados
3. Reporte de archivos
4. Eliminar TODOS los duplicados
5. Visualizar folder de duplicados
6. Salir
==================================================
            """)
        print("=" * 50)
        choice = input("Selecciona una opción (1-6): ")

        if choice == '1':
            print("\nEjecutando organización por tipo...\n")
            organize_photos_by_type(SOURCE_DIR, OUTPUT_DIR)
            input("\n✅ Proceso terminado. Presiona ENTER para continuar...")
        elif choice == '2':
            print("\nBuscando duplicados...\n")
            find_and_remove_duplicates(SOURCE_DIR, BACKUP_DIR)
            open_folder(BACKUP_DIR)
            input("\n✅ Limpieza completada. Presiona ENTER para continuar...")
        elif choice == '3':
            print("\n📊 Analizando resultados...\n")
            report = analyze_directory(BACKUP_DIR)
            print_report("REPORTE DE DUPLICADOS ELIMINADOS", report)
            input("\nPresiona ENTER para continuar...")
        elif option == "4":
            confirm = input(
                "\n⚠️ ESTA ACCIÓN ES IRREVERSIBLE ⚠️\n"
                "Se eliminarán TODOS los archivos en 'Duplicados_Eliminados'.\n"
                "¿Deseas continuar? (yes/no): "
            )

            if confirm.lower() == "yes":
                delete_all_duplicates(DUPLICATES_DIR)
            else:
                print("❎ Operación cancelada.")

            input("\nPresiona ENTER para continuar...")
        elif choice == '5':
            open_folder(BACKUP_DIR)
            sys.exit()
        elif choice == '6':
            print("Saliendo del programa. 👋")
            sys.exit()
        else:
            input("Opción inválida. Presiona ENTER para intentar nuevamente.")

def open_folder(path):
    """Abre un directorio según el sistema operativo."""
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", path])
    elif sys.platform == "win32":  # Windows
        os.startfile(path)
    elif sys.platform.startswith("linux"):  # Linux
        subprocess.run(["xdg-open", path])
    else:
        print(f"⚠️ No se puede abrir automáticamente en este sistema: {sys.platform}")

if __name__ == "__main__":
    main_menu()