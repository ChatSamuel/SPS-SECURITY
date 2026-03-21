"""
ENGINE 1: HASH
Lista de "procurados".
Se bater = malware confirmado.
"""

from pathlib import Path
from .base import BaseEngine, EngineResult
from ..utils.hashing import compute_sha256

MALWARE_HASHES = {
    "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f":
        "EICAR-Test-File",
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
        "EmptyFile-Suspicious",
}


class HashEngine(BaseEngine):
    name = "hash"
    weight = 3

    def analyze(self, filepath: Path) -> EngineResult:
        try:
            sha256 = compute_sha256(filepath)
            if not sha256:
                return self._error("Erro ao calcular hash")

            if sha256 in MALWARE_HASHES:
                return self._detected(
                    MALWARE_HASHES[sha256],
                    f"SHA256: {sha256[:32]}..."
                )

            return self._clean("Hash limpo")

        except Exception as e:
            return self._error(str(e))
