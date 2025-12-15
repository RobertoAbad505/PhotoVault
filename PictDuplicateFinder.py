import os
import hashlib
import shutil

EXCLUDED_DIRS = {
    "formats",
    "Duplicados_detectados",
    "Duplicados_Eliminados"
}

def hash_file(file_path):
    """Genera un hash MD5 para comparar archivos por contenido."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except Exception as e:
        print(f"⚠️ Error al leer {file_path}: {e}")
        return None
    return hash_md5.hexdigest()


def find_and_remove_duplicates(source_dir, backup_dir):
    """Detecta archivos duplicados y los mueve a una carpeta de respaldo."""

    source_dir = os.path.abspath(source_dir)
    backup_dir = os.path.abspath(backup_dir)

    print(f"🔍 Buscando duplicados en: {source_dir}")
    print(f"📦 Duplicados se moverán a: {backup_dir}\n")

    # Crear carpeta de respaldo y archivo .noindex
    os.makedirs(backup_dir, exist_ok=True)
    noindex_path = os.path.join(backup_dir, ".noindex")
    if not os.path.exists(noindex_path):
        open(noindex_path, "a").close()
        print(f"🛡️ Carpeta marcada como no indexable: {backup_dir}\n")

    hashes = {}
    duplicates_found = 0
    moved_files = 0

    for root, dirs, files in os.walk(source_dir):
        # Excluir carpetas NO deseadas modificando dirs
        dirs[:] = [
            d for d in dirs
            if d not in EXCLUDED_DIRS
        ]

        for filename in files:
            file_path = os.path.join(root, filename)

            if not os.path.isfile(file_path):
                continue

            file_hash = hash_file(file_path)
            if not file_hash:
                continue

            if file_hash in hashes:
                duplicates_found += 1
                dest_path = os.path.join(backup_dir, filename)

                counter = 1
                while os.path.exists(dest_path):
                    name, ext = os.path.splitext(filename)
                    dest_path = os.path.join(
                        backup_dir, f"{name}_{counter}{ext}"
                    )
                    counter += 1

                try:
                    shutil.move(file_path, dest_path)
                    moved_files += 1
                    print(f"📁 Duplicado movido: {file_path} → {dest_path}")
                except Exception as e:
                    print(f"⚠️ Error al mover {file_path}: {e}")
            else:
                hashes[file_hash] = file_path

    print("\n📊 --- REPORTE FINAL ---")
    print(f"Archivos únicos encontrados: {len(hashes)}")
    print(f"Duplicados detectados: {duplicates_found}")
    print(f"Duplicados movidos: {moved_files}")
    print(f"Respaldo en: {backup_dir}")
    print("\n✅ Proceso completado sin eliminar ningún archivo.")
