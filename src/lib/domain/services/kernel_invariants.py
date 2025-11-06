from __future__ import annotations
"""
File: src/lib/domain/services/kernel_invariants.py
Status: 🔄 WIP
Guards for kernel invariants (symmetry, weights, partition soundness).
Raise ValueError with actionable messages on violation.
"""
from typing import Set
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition

def assert_symmetric(g: Graph) -> None:
    for u, nbrs in g.adj.items():
        for v, w in nbrs.items():
            w_back = g.adj.get(v, {}).get(u)
            if w_back is None or w_back != w:
                raise ValueError(f"Asymmetric adjacency: w({u},{v})={w} != w({v},{u})={w_back}")

def assert_non_negative_weights(g: Graph) -> None:
    for u, nbrs in g.adj.items():
        for v, w in nbrs.items():
            if w < 0:
                raise ValueError(f"Negative weight on edge ({u},{v}): {w}")

def assert_partition_sound(g: Graph, p: Partition) -> None:
    g_nodes: Set[object] = set(g.nodes())
    p_nodes: Set[object] = set(p.node2com.keys())

    missing = g_nodes - p_nodes
    if missing:
        raise ValueError(f"Partition missing nodes: {missing}")

    extras = p_nodes - g_nodes
    if extras:
        raise ValueError(f"Partition contains nodes not in graph: {extras}")

    # node2com and com2nodes consistency
    for cid in p.community_ids():
        members = p.members(cid)
        for v in members:
            if p.node2com.get(v) != cid:
                raise ValueError(f"Inconsistent mapping for node {v}: node2com={p.node2com.get(v)} vs membership={cid}")

def validate(g: Graph, p: Partition) -> None:
    assert_symmetric(g)
    assert_non_negative_weights(g)
    assert_partition_sound(g, p)
