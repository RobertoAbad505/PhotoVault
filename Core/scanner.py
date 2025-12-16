import os
from typing import Callable, Iterator, Optional
from Core.utils import should_exclude_dir
from Core.models.photo import PhotoFile


def scan_photos(
    root_dir: str,
    on_event: Optional[Callable[[dict], None]] = None
) -> Iterator[PhotoFile]:
    """
    Escanea recursivamente el filesystem y produce PhotoFile.
    Emite eventos de progreso si se provee on_event.
    """

    scanned = 0

    for root, dirs, files in os.walk(root_dir):
        # Excluir carpetas no deseadas
        if should_exclude_dir(root):
            continue

        for filename in files:
            full_path = os.path.join(root, filename)

            if not os.path.isfile(full_path):
                continue

            try:
                photo = PhotoFile.from_path(full_path)
                scanned += 1

                # Emitir progreso
                if on_event:
                    on_event({
                        "type": "scan_progress",
                        "count": scanned,
                        "path": full_path
                    })

                yield photo

            except Exception as e:
                if on_event:
                    on_event({
                        "type": "scan_error",
                        "path": full_path,
                        "error": str(e)
                    })
                continue

    # Evento final
    if on_event:
        on_event({
            "type": "scan_complete",
            "total": scanned
        })
