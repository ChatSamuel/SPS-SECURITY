"""
engines/base.py
O "molde" que todo engine deve seguir.
Garante que todos retornam resultado no mesmo formato.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EngineResult:
    engine_name: str
    status: str       # CLEAN | SUSPICIOUS | DETECTED | ERROR | SKIPPED
    score: int        # 0=limpo, 1=suspeito, 2=detectado
    threat_name: str | None = None
    details: str = ""

    @property
    def is_threat(self):
        return self.status == "DETECTED"

    def to_dict(self):
        return {
            "engine": self.engine_name,
            "status": self.status,
            "score": self.score,
            "threat_name": self.threat_name,
            "details": self.details,
        }


class BaseEngine(ABC):
    name: str = "base"
    weight: int = 1

    @abstractmethod
    def analyze(self, filepath: Path) -> EngineResult:
        ...

    def _error(self, msg):
        return EngineResult(self.name, "ERROR", 0, details=msg)

    def _clean(self, details=""):
        return EngineResult(self.name, "CLEAN", 0, details=details)

    def _suspicious(self, details="", threat_name=None):
        return EngineResult(self.name, "SUSPICIOUS", 1,
                            threat_name=threat_name, details=details)

    def _detected(self, threat_name, details=""):
        return EngineResult(self.name, "DETECTED", 2,
                            threat_name=threat_name, details=details)
