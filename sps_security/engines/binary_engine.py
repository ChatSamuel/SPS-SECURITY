"""
ENGINE 4: BINARY
Analisa estrutura do arquivo e detecta padrões binários suspeitos.
"""

import math
from pathlib import Path
from .base import BaseEngine, EngineResult


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    e = 0.0
    n = len(data)
    for c in counts:
        if c > 0:
            p = c / n
            e -= p * math.log2(p)
    return e


class BinaryEngine(BaseEngine):
    name = "binary"
    weight = 2

    def analyze(self, filepath: Path) -> EngineResult:
        try:
            size = filepath.stat().st_size
            if size == 0:
                return self._clean("Arquivo vazio")

            content = filepath.read_bytes()

            score = 0

            # Detecta executável (MZ header)
            if content[:2] == b"MZ":
                score += 2

            # Alta entropia (arquivo suspeito/compactado)
            e = entropy(content[:4096])
            if e > 7.5:
                score += 1

            if score == 0:
                return self._clean("Binário normal")

            elif score <= 2:
                return self._suspicious("Binário suspeito")

            else:
                return self._detected("Binary-Malicious", "Alta entropia + executável")

        except Exception as e:
            return self._error(str(e))
