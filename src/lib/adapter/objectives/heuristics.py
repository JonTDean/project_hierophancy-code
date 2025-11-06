from __future__ import annotations
"""
File: src/lib/adapter/objectives/heuristics.py
Objective: Wrap existing neighbor-weight heuristic delta in ObjectivePort.
Score is a simple intra-community weight sum (for diagnostics only).
"""
from src.lib.port.objective import ObjectivePort
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.delta import DeltaFn
from src.lib.adapter.heuristics.neighbor_weight_delta import (
    heuristic_delta_by_neighbor_weight,
)

class HeuristicNeighborWeightObjective(ObjectivePort):
    def score(self, g: Graph, p: Partition) -> float:
        s = 0.0
        for cid in p.community_ids():
            C = set(p.members(cid))
            for u in C:
                for v, w in g.adj.get(u, {}).items():
                    if v in C:
                        s += w
        return s

    def delta_fn(self, g: Graph, p: Partition) -> DeltaFn:
        # Directly expose the existing heuristic delta (not guaranteed to match score diff).
        return heuristic_delta_by_neighbor_weight
