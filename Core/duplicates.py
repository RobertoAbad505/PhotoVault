from typing import Iterable, Callable, Optional, Dict, List
from Core.models.photo import PhotoFile
import hashlib


def _hash_file(path: str) -> str:
    """Hash MD5 por chunks para archivos grandes."""
    hash_md5 = hashlib.md5()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def detect_duplicates(
    photos: Iterable[PhotoFile],
    on_event: Optional[Callable[[dict], None]] = None
) -> Dict[str, dict]:
    """
    Detecta duplicados por contenido (hash).
    """

    hashes: Dict[str, PhotoFile] = {}
    duplicates: Dict[str, List[PhotoFile]] = {}

    processed = 0

    for photo in photos:
        processed += 1

        try:
            file_hash = _hash_file(photo.path)
            photo.hash = file_hash

            if file_hash in hashes:
                duplicates.setdefault(file_hash, []).append(photo)

                if on_event:
                    on_event({
                        "type": "duplicate_found",
                        "hash": file_hash,
                        "path": photo.path
                    })
            else:
                hashes[file_hash] = photo

                if on_event:
                    on_event({
                        "type": "unique_found",
                        "hash": file_hash,
                        "path": photo.path
                    })

        except Exception as e:
            if on_event:
                on_event({
                    "type": "hash_error",
                    "path": photo.path,
                    "error": str(e)
                })

        if on_event and processed % 50 == 0:
            on_event({
                "type": "duplicate_progress",
                "processed": processed,
                "unique": len(hashes),
                "duplicates": sum(len(v) for v in duplicates.values())
            })

    if on_event:
        on_event({
            "type": "duplicate_complete",
            "processed": processed,
            "unique": len(hashes),
            "duplicates": sum(len(v) for v in duplicates.values())
        })

    return {
        "unique": hashes,
        "duplicates": duplicates
    }
