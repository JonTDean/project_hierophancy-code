from __future__ import annotations
from typing import Dict

from src.lib.domain.services.graph import merge_nodes_subset
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.general import CommunityId
from src.lib.domain.types.delta import DeltaFn

def singleton_partition(G: Graph) -> Partition:
    return Partition({v: v for v in G.nodes()})

def lift_partition_to_aggregated(P_old: Partition, P_refined: Partition) -> Partition:
    agg_nodes = [frozenset(P_refined.members(cid)) for cid in P_refined.community_ids()]
    mapping: Dict[NodeLike, CommunityId] = {}
    for supernode in agg_nodes:
        representative: NodeLike = next(iter(supernode))
        mapping[supernode] = P_old.community_of(representative)
    return Partition(mapping)

def refine_partition(
    G: Graph,
    P: Partition,
    delta_fn: DeltaFn,
    gamma: float,
    theta: float,
) -> Partition:
    Prefined = singleton_partition(G)
    for cid in P.community_ids():
        C = set(P.members(cid))
        Prefined = merge_nodes_subset(G, Prefined, C, delta_fn, gamma, theta)
    return Prefined
