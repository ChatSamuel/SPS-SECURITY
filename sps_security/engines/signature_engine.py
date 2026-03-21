"""
ENGINE 2: SIGNATURE
Procura padrões suspeitos dentro do arquivo.
"""

from pathlib import Path
from .base import BaseEngine, EngineResult

SIGNATURES = [
    (b"X5O!P%@AP[4\\PZX54(P^)7CC)7}", "EICAR-Test", 3),
    (b"powershell -nop -w hidden", "PowerShell-Hidden", 3),
    (b"powershell -enc", "PowerShell-Encoded", 2),
    (b"meterpreter", "Metasploit", 3),
    (b"CreateRemoteThread", "Process Injection", 3),
    (b"VirtualAllocEx", "Memory Injection", 2),
]

MAX_SIZE = 50 * 1024 * 1024


class SignatureEngine(BaseEngine):
    name = "signature"
    weight = 2

    def analyze(self, filepath: Path) -> EngineResult:
        try:
            if filepath.stat().st_size > MAX_SIZE:
                return EngineResult(self.name, "SKIPPED", 0,
                                    details="Arquivo grande")

            content = filepath.read_bytes()
            hits = []

            for pattern, name, weight in SIGNATURES:
                if pattern.lower() in content.lower():
                    hits.append((name, weight))

            if not hits:
                return self._clean("Sem assinaturas")

            total = sum(w for _, w in hits)
            top = max(hits, key=lambda x: x[1])

            if total >= 3:
                return self._detected(top[0], "Assinatura maliciosa")

            return self._suspicious("Possível ameaça", top[0])

        except Exception as e:
            return self._error(str(e))
