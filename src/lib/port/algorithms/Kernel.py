from __future__ import annotations
"""
File: src/lib/port/algorithms/Kernel.py
Port: Shared algorithm kernel (move/refine/aggregate/multi_level)
Status: 🔄 WIP

Invariants:
- Graph is undirected weighted (adj[u][v] == adj[v][u]).
- Supernodes are frozenset[NodeLike] (nesting allowed); domain services accept/return them.
- Determinism is controlled by the kernel's RNG seed.
"""
from dataclasses import dataclass
from typing import Protocol, Optional, Callable
from src.lib.domain.types.delta import DeltaFn
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition

@dataclass
class KernelEvents:
    """
    Lightweight, phase-scoped instrumentation.
    Counts are best-effort without modifying domain services:
    - moves_tried: # of delta evaluations (proxy for attempts)
    - moves_applied: # of vertices whose community changed in this phase
    - deltas_positive: # of delta evaluations > 0
    """
    phase: str                       # 'local_move' | 'refine' | 'aggregate' | 'level_end' | 'done'
    level_index: int
    moves_tried: int = 0
    moves_applied: int = 0
    deltas_positive: int = 0
    seconds_phase: float = 0.0
    cumulative_seconds: float = 0.0
    communities: int = 0
    nodes: int = 0
    seed: Optional[int] = None

ProgressCallback = Callable[[KernelEvents], None]

class KernelPort(Protocol):
    def local_move(self, g: Graph, p: Partition, delta_fn: DeltaFn) -> Partition: ...
    def refine(
        self,
        g: Graph,
        p: Partition,
        *,
        delta_fn: DeltaFn,
        gamma: float,
        theta: float,
    ) -> Partition: ...
    def aggregate(self, g: Graph, p_refined: Partition) -> Graph: ...
    def multi_level(
        self,
        g: Graph,
        p0: Partition,
        *,
        delta_fn: DeltaFn,
        gamma: float,
        theta: float,
        max_levels: int,
    ) -> Partition: ...
