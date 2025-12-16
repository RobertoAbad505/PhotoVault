import os
import shutil

PICTURES_DIR = "/Users/RobertoAbad/Pictures"
LEGACY_DIR = os.path.join(PICTURES_DIR, "formats")

MEDIA_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".heic", ".tiff", ".bmp", ".gif",
    ".raw", ".cr2", ".nef", ".arw", ".dng",
    ".mov", ".mp4", ".m4v", ".avi", ".mkv"
}

def is_media_file(filename: str) -> bool:
    return os.path.splitext(filename.lower())[1] in MEDIA_EXTENSIONS

def restore_media_and_delete_legacy():
    if not os.path.exists(LEGACY_DIR):
        print("✅ No existe carpeta 'formats'. Nada que limpiar.")
        return

    print("\n🔥 LIMPIEZA HARD LEGACY (SIN BACKUP)")
    print(f"Procesando: {LEGACY_DIR}\n")

    restored = 0
    deleted = 0

    for root, _, files in os.walk(LEGACY_DIR):
        for file in files:
            src = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            if is_media_file(file):
                dst = os.path.join(PICTURES_DIR, file)

                if os.path.exists(dst):
                    os.remove(src)
                    deleted += 1
                    print(f"❌ Duplicado eliminado: {src}")
                else:
                    shutil.move(src, dst)
                    restored += 1
                    print(f"📸 Restaurado: {file}")
            else:
                os.remove(src)
                deleted += 1
                print(f"🗑️ Config eliminado: {file}")

    # Eliminar TODA la carpeta legacy
    shutil.rmtree(LEGACY_DIR)
    print("\n🧹 Carpeta 'formats' eliminada completamente")

    print("\n📊 RESUMEN FINAL")
    print(f"📸 Multimedia restaurado : {restored}")
    print(f"🗑️ Archivos eliminados  : {deleted}")
    print("\n✅ Limpieza completada")

if __name__ == "__main__":
    restore_media_and_delete_legacy()
