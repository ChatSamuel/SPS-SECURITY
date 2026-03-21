"""
ENGINE 3: HEURISTIC
Detecta padrões suspeitos pelo nome e tipo do arquivo.
"""

from pathlib import Path
from .base import BaseEngine, EngineResult

DANGEROUS_EXT = {".exe", ".bat", ".cmd", ".vbs", ".js", ".ps1"}

SUSPICIOUS_NAMES = [
    "virus", "trojan", "hack", "crack", "keygen", "payload"
]


class HeuristicEngine(BaseEngine):
    name = "heuristic"
    weight = 1

    def analyze(self, filepath: Path) -> EngineResult:
        try:
            score = 0
            name = filepath.name.lower()

            # Nome suspeito
            for word in SUSPICIOUS_NAMES:
                if word in name:
                    score += 2

            # Extensão perigosa
            if filepath.suffix.lower() in DANGEROUS_EXT:
                score += 1

            if score == 0:
                return self._clean("Arquivo normal")

            elif score <= 2:
                return self._suspicious("Levemente suspeito")

            else:
                return self._detected("Heuristic-High", "Comportamento suspeito")

        except Exception as e:
            return self._error(str(e))
