from __future__ import annotations
from collections import deque, defaultdict
from typing import Optional, List, Tuple, Set, Dict, FrozenSet
import math
import random

from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.types.delta import DeltaFn
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.general import CommunityId

def aggregate_graph(G: Graph, P_refined: Partition) -> Graph:
    """
    Contract: sum *every* underlying undirected edge exactly once into the supergraph.
    This avoids under-counting when multiple base edges map to the same (su, sv).
    """
    # Map base nodes to supernodes
    comm_nodes = [frozenset(P_refined.members(cid)) for cid in P_refined.community_ids()]
    node_to_super: Dict[NodeLike, FrozenSet[NodeLike]] = {}
    for supernode in comm_nodes:
        for u in supernode:
            node_to_super[u] = supernode

    # Accumulate weights per supernode pair, counting each base edge once
    pair_weights: Dict[Tuple[FrozenSet[NodeLike], FrozenSet[NodeLike]], float] = defaultdict(float)
    visited_base_pairs: Set[FrozenSet[NodeLike]] = set()

    for u in G.nodes():
        for v, w in G.adj.get(u, {}).items():
            uv = frozenset((u, v))
            if uv in visited_base_pairs:
                continue  # already counted the undirected edge (u,v)
            visited_base_pairs.add(uv)
            su = node_to_super[u]
            sv = node_to_super[v]
            pair_weights[(su, sv)] += w

    G2 = Graph()
    for (su, sv), w in pair_weights.items():
        G2.add_edge(su, sv, w)
    return G2

def move_nodes_fast(G: Graph, P: Partition, delta_fn: DeltaFn) -> Partition:
    nodes = list(G.nodes())
    random.shuffle(nodes)
    Q = deque(nodes)
    in_queue: Set[NodeLike] = set(nodes)

    while Q:
        v = Q.popleft()
        in_queue.discard(v)

        neighbor_comms = {P.community_of(u) for u in G.neighbors(v)}
        candidate_comms: List[Optional[CommunityId]] = list(neighbor_comms)
        candidate_comms.append(P.community_of(v))
        candidate_comms.append(None)  # None => new singleton community

        best_C: Optional[CommunityId] = None
        best_delta = float("-inf")
        for C in candidate_comms:
            delta = delta_fn(G, P, v, C)
            if delta > best_delta:
                best_delta, best_C = delta, C

        if best_delta > 0:
            dest = P.move(v, best_C)
            P.drop_empty()
            N = {u for u in G.neighbors(v) if P.community_of(u) != dest}
            for u in N:
                if u not in in_queue:
                    Q.append(u)
                    in_queue.add(u)

    return P

def merge_nodes_subset(
    G: Graph,
    P: Partition,
    S: Set[NodeLike],
    delta_fn: DeltaFn,
    gamma: float,
    theta: float,
) -> Partition:
    def S_minus(X: Set[NodeLike]) -> Set[NodeLike]:
        return set(S) - set(X)

    R: List[NodeLike] = []
    vol_S = G.volume(S)

    for v in S:
        ev = G.cut_weight({v}, S_minus({v}))
        lhs = ev
        rhs = gamma * G.volume({v}) * (vol_S - G.volume({v}))
        if lhs >= rhs:
            R.append(v)

    random.shuffle(R)

    for v in R:
        if not P.is_singleton(v):
            continue

        T: List[CommunityId] = []
        for cid in P.community_ids():
            C = P.members(cid)
            if not C.issubset(S):
                continue
            e_cut = G.cut_weight(C, S_minus(C))
            lhs = e_cut
            rhs = gamma * G.volume(C) * (vol_S - G.volume(C))
            if lhs >= rhs:
                T.append(cid)

        if not T:
            continue

        deltas: List[Tuple[CommunityId, float]] = []
        for cid in T:
            d = delta_fn(G, P, v, cid)
            if d >= 0:
                deltas.append((cid, d))

        if not deltas:
            continue

        weights = [math.exp(d / max(theta, 1e-12)) for (_, d) in deltas]
        total = sum(weights)
        r = random.random() * total
        acc = 0.0
        chosen: Optional[CommunityId] = None
        for (cid, _d), w in zip(deltas, weights):
            acc += w
            if r <= acc:
                chosen = cid
                break
        chosen = chosen if chosen is not None else deltas[-1][0]

        P.move(v, chosen)
        P.drop_empty()

    return P
