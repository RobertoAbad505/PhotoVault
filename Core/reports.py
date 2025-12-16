from typing import Iterable, Dict
from collections import defaultdict
from Core.models.photo import PhotoFile


def generate_report(photos: Iterable[PhotoFile]) -> Dict:
    """
    Genera métricas generales para una colección de archivos.
    """

    total_files = 0
    total_size = 0

    by_extension = defaultdict(lambda: {"count": 0, "size": 0})
    by_folder = defaultdict(lambda: {"count": 0, "size": 0})

    for photo in photos:
        total_files += 1
        total_size += photo.size

        ext = photo.extension.lower() if photo.extension else "no_ext"
        folder = photo.path.rsplit("/", 1)[0]

        by_extension[ext]["count"] += 1
        by_extension[ext]["size"] += photo.size

        by_folder[folder]["count"] += 1
        by_folder[folder]["size"] += photo.size

    return {
        "total_files": total_files,
        "total_size": total_size,
        "by_extension": dict(by_extension),
        "by_folder": dict(by_folder),
    }


def summarize_duplicates(duplicates: Dict[str, list[PhotoFile]]) -> Dict:
    """
    Resume duplicados detectados.
    """

    all_duplicates = []
    for group in duplicates.values():
        all_duplicates.extend(group)

    return generate_report(all_duplicates)

def print_report(title: str, report: Dict):
    print("\n" + "=" * 50)
    print(f"📊 {title}")
    print("=" * 50)

    print(f"Total archivos : {report['total_files']}")
    print(f"Total tamaño   : {report['total_size'] / (1024**3):.2f} GB\n")

    print("📁 Por tipo:")
    for ext, data in sorted(
        report["by_extension"].items(),
        key=lambda x: x[1]["size"],
        reverse=True
    ):
        size_gb = data["size"] / (1024**3)
        print(f"{ext:8} → {data['count']:6} archivos | {size_gb:6.2f} GB")
