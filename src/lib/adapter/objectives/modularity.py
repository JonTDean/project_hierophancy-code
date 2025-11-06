from __future__ import annotations

"""
File: src/lib/adapter/objectives/modularity.py
Objective: Weighted Newman–Girvan modularity (loops allowed).
Uses W = sum of degrees (works for loops under our Graph).
"""
from typing import Set
from src.lib.port.objective import ObjectivePort
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.delta import DeltaFn
from src.lib.domain.types.nodes import NodeLike

def _total_degree(g: Graph) -> float:
    return sum(g.degree(u) for u in g.nodes())

def _community_internal_weight_doublecount(g: Graph, C: Set[NodeLike]) -> float:
    # sum_{i in C} sum_{j in C} A_ij (off-diagonals counted twice, loops once)
    w = 0.0
    Cset = set(C)
    for i in Cset:
        for j, wij in g.adj.get(i, {}).items():
            if j in Cset:
                w += wij
    return w

def _community_degree_sum(g: Graph, C: Set[NodeLike]) -> float:
    return sum(g.degree(i) for i in C)

class ModularityObjective(ObjectivePort):
    def score(self, g: Graph, p: Partition) -> float:
        W = _total_degree(g)
        if W <= 0:
            return 0.0
        s = 0.0
        for cid in p.community_ids():
            C = p.members(cid)
            sum_A = _community_internal_weight_doublecount(g, C)
            sum_k = _community_degree_sum(g, C)
            s += (sum_A / W) - (sum_k * sum_k) / (W * W)
        return s

    def delta_fn(self, g: Graph, p: Partition) -> DeltaFn:
        def _delta(G: Graph, P: Partition, v, dest) -> float:
            cur = P.community_of(v)
            if dest == cur:
                return 0.0
            # clone + move, then compute score diff (exact but O(n))
            P2 = Partition(dict(P.node2com))
            P2.move(v, dest)  # dest=None => new community via Partition API
            return self.score(G, P2) - self.score(G, P)
        return _delta
