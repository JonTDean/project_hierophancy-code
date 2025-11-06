from __future__ import annotations
"""
File: src/lib/port/objective.py
Port: Objective (global score + per-move delta function)
"""
from typing import Protocol
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.delta import DeltaFn

class ObjectivePort(Protocol):
    def delta_fn(self, g: Graph, p: Partition) -> DeltaFn: ...
    def score(self, g: Graph, p: Partition) -> float: ...
