import os
import shutil
from typing import Iterable, Callable, Optional, Dict
from datetime import datetime
from Core.models.photo import PhotoFile

SPECIAL_FORMATS = {"cr2", "nef", "arw", "dng", "raf", "raw"}


def _build_destination(photo: PhotoFile, base_dir: str) -> str:
    date = photo.created_at or datetime.now()
    year = str(date.year)
    month = f"{date.month:02d}"

    dest_dir = os.path.join(base_dir, year, month)

    if photo.extension.lower() in SPECIAL_FORMATS:
        dest_dir = os.path.join(dest_dir, "RAW")

    os.makedirs(dest_dir, exist_ok=True)

    return os.path.join(dest_dir, photo.name)


def organize_photos(
    photos: Iterable[PhotoFile],
    base_dir: str,
    mode: str = "simulate",
    on_event: Optional[Callable[[dict], None]] = None
) -> Dict:
    """
    Organiza archivos por año/mes/(RAW).
    """

    assert mode in {"simulate", "report", "execute"}

    moved = 0
    skipped = 0
    planned = []

    for photo in photos:
        dest = _build_destination(photo, base_dir)

        if photo.path == dest:
            skipped += 1
            continue

        planned.append((photo.path, dest))

        if on_event:
            on_event({
                "type": "organize_planned",
                "source": photo.path,
                "destination": dest
            })

    if mode == "report":
        return {
            "planned": len(planned),
            "skipped": skipped
        }

    if mode == "execute":
        for src, dst in planned:
            try:
                shutil.move(src, dst)
                moved += 1

                if on_event:
                    on_event({
                        "type": "organize_moved",
                        "source": src,
                        "destination": dst
                    })
            except Exception as e:
                if on_event:
                    on_event({
                        "type": "organize_error",
                        "source": src,
                        "error": str(e)
                    })

    if on_event:
        on_event({
            "type": "organize_complete",
            "planned": len(planned),
            "moved": moved,
            "skipped": skipped
        })

    return {
        "planned": len(planned),
        "moved": moved,
        "skipped": skipped
    }
