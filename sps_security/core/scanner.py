"""
core/scanner.py
Percorre diretórios e envia arquivos para o MultiEngine.
"""

import os
from pathlib import Path

from .multi_engine import MultiEngine


class Scanner:

    def __init__(self):
        self.engine = MultiEngine()

    def scan(self, path):

        path = Path(path)

        files = []

        if path.is_file():
            files.append(path)
        else:
            for root, _, filenames in os.walk(path):
                for f in filenames:
                    files.append(Path(root) / f)

        total = len(files)
        threats = 0

        print("\n[SCAN] Starting analysis...\n")

        for i, file in enumerate(files, 1):

            result = self.engine.analyze_file(file)

            if result["risk"] in ("HIGH", "CRITICAL"):
                threats += 1
                print(f"[THREAT] {file} -> {result['risk']} (score={result['score']})")

        print("\n[RESULT]")
        print(f"Files scanned: {total}")
        print(f"Threats found: {threats}")
