from __future__ import annotations
from typing import Optional
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.types.general import CommunityId

def heuristic_delta_by_neighbor_weight(
    G: Graph,
    P: Partition,
    v: NodeLike,
    dest: Optional[CommunityId],
) -> float:
    """
    Simple (not theoretically exact) delta: prefer communities with higher total
    edge weight from v. Leaving current community is penalized by comparison.
    Treat dest=None as a fresh singleton with zero internal connectivity.
    """
    cur = P.community_of(v)
    if dest == cur:
        return 0.0

    def total_weight_to(comm_id: Optional[CommunityId]) -> float:
        if comm_id is None:
            return 0.0
        members = P.members(comm_id)
        return sum(G.weight(v, u) for u in members if u != v)

    w_cur = total_weight_to(cur)
    w_new = total_weight_to(dest)
    return w_new - w_cur
