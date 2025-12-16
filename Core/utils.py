import os
from pathlib import Path

# Directorios que nunca deben procesarse
EXCLUDED_DIR_NAMES = {
    "formats",
    "Duplicados_detectados",
    "Duplicados_Eliminados",
    ".git",
    "__pycache__"
}

def normalize_path(path: str | Path) -> Path:
    """
    Normaliza una ruta a Path absoluto.
    """
    return Path(path).expanduser().resolve()

def should_exclude_dir(dir_path: str | Path) -> bool:
    """
    Retorna True si el directorio debe excluirse del procesamiento.
    """
    path = normalize_path(dir_path)

    for part in path.parts:
        if part in EXCLUDED_DIR_NAMES:
            return True

    return False
