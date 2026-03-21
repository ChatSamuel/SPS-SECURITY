"""
ENGINE 5: BEHAVIOR
Analisa comportamento suspeito em scripts.
"""

import re
from pathlib import Path
from .base import BaseEngine, EngineResult

PATTERNS = [
    (rb"exec\(", "Exec Code", 2),
    (rb"subprocess", "Subprocess Execution", 2),
    (rb"os\.system", "System Command", 2),
    (rb"socket\.connect", "Network Connection", 2),
    (rb"requests\.post", "Data Exfiltration", 3),
]

SCRIPT_EXT = {".py", ".sh", ".bat", ".ps1"}


class BehaviorEngine(BaseEngine):
    name = "behavior"
    weight = 2

    def analyze(self, filepath: Path) -> EngineResult:
        try:
            if filepath.suffix.lower() not in SCRIPT_EXT:
                return EngineResult(self.name, "SKIPPED", 0,
                                    details="Não é script")

            content = filepath.read_bytes()
            hits = []

            for pattern, name, weight in PATTERNS:
                if re.search(pattern, content):
                    hits.append((name, weight))

            if not hits:
                return self._clean("Comportamento normal")

            score = sum(w for _, w in hits)
            top = max(hits, key=lambda x: x[1])

            if score >= 3:
                return self._detected(top[0], "Comportamento malicioso")

            return self._suspicious("Comportamento suspeito", top[0])

        except Exception as e:
            return self._error(str(e))
