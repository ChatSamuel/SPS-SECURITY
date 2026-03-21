"""
utils/hashing.py
Calcula a "impressão digital" de arquivos.
Dois arquivos iguais = mesma impressão digital.
Malware conhecido tem impressão registrada.
"""

import hashlib
from pathlib import Path


def compute_sha256(filepath) -> str | None:
    """Calcula SHA256 de um arquivo."""
    try:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def compute_md5(filepath) -> str | None:
    """Calcula MD5 (mais rápido, usado para cache)."""
    try:
        h = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None
