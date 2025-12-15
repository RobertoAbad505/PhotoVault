# delete_duplicates.py

import os
import shutil

def delete_all_duplicates(duplicates_dir: str):
    if not os.path.exists(duplicates_dir):
        print(f"❌ La carpeta no existe: {duplicates_dir}")
        return

    total_files = 0
    total_size = 0

    print(f"\n🧹 Eliminando duplicados en:\n{duplicates_dir}\n")

    for root, dirs, files in os.walk(duplicates_dir):
        for file in files:
            path = os.path.join(root, file)
            try:
                size = os.path.getsize(path)
                os.remove(path)
                total_files += 1
                total_size += size
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {path}: {e}")

    # Limpia carpetas vacías
    for root, dirs, _ in os.walk(duplicates_dir, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    gb = total_size / (1024 ** 3)

    print("✅ ELIMINACIÓN COMPLETADA")
    print("-" * 40)
    print(f"Archivos eliminados : {total_files}")
    print(f"Espacio liberado    : {gb:.2f} GB\n")
