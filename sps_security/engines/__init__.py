from .base import BaseEngine, EngineResult
from .hash_engine import HashEngine
from .signature_engine import SignatureEngine
from .heuristic_engine import HeuristicEngine
from .binary_engine import BinaryEngine
from .behavior_engine import BehaviorEngine

ALL_ENGINES = [
    HashEngine,
    SignatureEngine,
    HeuristicEngine,
    BinaryEngine,
    BehaviorEngine,
]
