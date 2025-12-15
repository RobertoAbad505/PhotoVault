import os
import shutil

def organize_photos_by_type(source_dir, output_dir):
    """
    Organiza las fotos por extensión en subcarpetas dentro de output_dir.
    """
    print(f"📂 Iniciando organización desde: {source_dir}")
    print(f"📁 Archivos organizados se guardarán en: {output_dir}\n")

    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            # Filtrar solo archivos (evita carpetas ocultas u otros directorios)
            if not os.path.isfile(file_path):
                continue

            file_ext = os.path.splitext(filename)[1].lower().strip('.')
            if not file_ext:
                file_ext = "otros"

            dest_folder = os.path.join(output_dir, file_ext)
            os.makedirs(dest_folder, exist_ok=True)

            dest_path = os.path.join(dest_folder, filename)

            # Evitar sobreescribir archivos existentes
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                counter += 1

            shutil.copy2(file_path, dest_path)
            print(f"✅ Copiado: {filename} → {dest_folder}")

    print("\n🎉 Organización completada.")
