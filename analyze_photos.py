import os
from collections import defaultdict

def analyze_directory(base_dir):
    file_count = 0
    total_size = 0
    by_extension = defaultdict(lambda: {"count": 0, "size": 0})
    by_folder = defaultdict(int)

    for root, _, files in os.walk(base_dir):
        for f in files:
            path = os.path.join(root, f)
            if not os.path.isfile(path):
                continue

            size = os.path.getsize(path)
            ext = os.path.splitext(f)[1].lower() or "no_ext"
            folder = os.path.relpath(root, base_dir)

            file_count += 1
            total_size += size
            by_extension[ext]["count"] += 1
            by_extension[ext]["size"] += size
            by_folder[folder] += size

    return file_count, total_size, by_extension, by_folder


def print_report(title, data):
    count, size, by_ext, by_folder = data

    print(f"\n📊 {title}")
    print("-" * 50)
    print(f"Total archivos : {count}")
    print(f"Total tamaño   : {size / (1024**3):.2f} GB\n")

    print("📁 Por tipo:")
    for ext, info in sorted(by_ext.items(), key=lambda x: x[1]["size"], reverse=True):
        print(f"{ext:6} → {info['count']:5} archivos | {info['size'] / (1024**3):6.2f} GB")

    print("\n📂 Por carpeta:")
    for folder, sz in sorted(by_folder.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{folder:30} {sz / (1024**3):6.2f} GB")


if __name__ == "__main__":
    BASE_DIR = "/Users/RobertoAbad/Pictures/formats/Duplicados_Eliminados"
    report = analyze_directory(BASE_DIR)
    print_report("REPORTE DE DUPLICADOS ELIMINADOS", report)
