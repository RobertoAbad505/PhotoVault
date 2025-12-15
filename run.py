import subprocess, sys, os
from PicSortType import organize_photos_by_type
from PictDuplicateFinder import find_and_remove_duplicates

# Rutas base (puedes modificarlas aquí)
SOURCE_DIR = r"/Users/RobertoAbad/Pictures"
OUTPUT_DIR = r"/Users/RobertoAbad/Pictures/formats/Duplicados_detectados"
BACKUP_DIR = r"/Users/RobertoAbad/Pictures/formats/Duplicados_Eliminados"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_console()
        print("=" * 50)
        print("📸 PHOTO ORGANIZER MENU")
        print("=" * 50)
        print("1. Organizar fotos por tipo (RAW, JPG, PNG, etc.)")
        print("2. Detectar y limpiar duplicados")
        print("3. Visualizar folder de duplicados")
        print("4. Salir")
        print("=" * 50)
        choice = input("Selecciona una opción (1-3): ")

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
            open_folder(BACKUP_DIR)
            sys.exit()
        elif choice == '4':
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