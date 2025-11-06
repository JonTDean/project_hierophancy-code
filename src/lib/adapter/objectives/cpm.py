from __future__ import annotations

"""
File: src/lib/adapter/objectives/cpm.py
Objective: Constant Potts Model (weighted).
Score: sum_C [ sum_{i,j in C} A_ij  - gamma * |C| (|C|-1) ]
We use the same "doublecount" convention as modularity for A_ij part.
"""
from typing import Set
from src.lib.port.objective import ObjectivePort
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.types.delta import DeltaFn

def _internal_weight_doublecount(g: Graph, C: Set[NodeLike]) -> float:
    w = 0.0
    Cset = set(C)
    for i in Cset:
        for j, wij in g.adj.get(i, {}).items():
            if j in Cset:
                w += wij
    return w

class CPMObjective(ObjectivePort):
    def __init__(self, gamma: float = 1.0) -> None:
        self.gamma = float(gamma)

    def with_gamma(self, gamma: float) -> "CPMObjective":
        return CPMObjective(gamma)

    def score(self, g: Graph, p: Partition) -> float:
        s = 0.0
        for cid in p.community_ids():
            C = p.members(cid)
            n = float(len(C))
            s += _internal_weight_doublecount(g, C) - self.gamma * (n * (n - 1.0))
        return s

    def delta_fn(self, g: Graph, p: Partition) -> DeltaFn:
        def _delta(G: Graph, P: Partition, v, dest) -> float:
            cur = P.community_of(v)
            if dest == cur:
                return 0.0
            P2 = Partition(dict(P.node2com))
            P2.move(v, dest)
            return self.score(G, P2) - self.score(G, P)
        return _delta
