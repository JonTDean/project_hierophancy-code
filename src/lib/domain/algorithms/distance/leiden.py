from __future__ import annotations
from typing import List, Set
from src.lib.domain.types.nodes import BaseNode
from src.lib.domain.types.delta import DeltaFn
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.services.graph import (
    move_nodes_fast,
    aggregate_graph,
)
from src.lib.domain.services.partition import (
    refine_partition, 
    lift_partition_to_aggregated
)


def leiden(
    g: Graph,
    p: Partition,
    delta_fn: DeltaFn,
    gamma: float = 1.0,
    theta: float = 1.0,
    max_levels: int = 100,
) -> List[Set[BaseNode]]:
    levels = 0
    while True:
        p = move_nodes_fast(g, p, delta_fn)
        done = (p.size() == len(g.nodes()))
        if not done and levels < max_levels:
            Prefined = refine_partition(g, p, delta_fn, gamma, theta)
            g = aggregate_graph(g, Prefined)
            p = lift_partition_to_aggregated(p, Prefined)
            levels += 1
            continue
        return p.flattened_partition()
