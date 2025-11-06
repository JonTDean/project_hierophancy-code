from __future__ import annotations
"""
File: src/lib/adapter/objectives/conductance.py
Objective: Negative normalized cut (maximize = minimize cut/volume).
Score = - sum_C [ cut(C, ~C) / max(volume(C), 1e-12) ]
"""
from src.lib.port.objective import ObjectivePort
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.delta import DeltaFn

class ConductanceObjective(ObjectivePort):
    def score(self, g: Graph, p: Partition) -> float:
        V = set(g.nodes())
        s = 0.0
        for cid in p.community_ids():
            C = set(p.members(cid))
            if not C:
                continue
            cut = g.cut_weight(C, V - C)
            vol = g.volume(C)
            s += -(cut / max(vol, 1e-12))
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
