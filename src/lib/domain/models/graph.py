from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Iterable
from src.lib.domain.types.positions import Adjacency
from src.lib.domain.types.nodes import NodeLike

def _adj_factory() -> Adjacency:
    return {}

@dataclass
class Graph:
    """
    Undirected weighted graph. Adjacency is symmetric: adj[u][v] == adj[v][u].
    Nodes may be base nodes (e.g., ints/strings) or aggregated nodes (frozensets of base nodes).
    """
    adj: Adjacency = field(default_factory=_adj_factory)
    def nodes(self) -> Set[NodeLike]:
        return set(self.adj.keys())

    def add_edge(self, u: NodeLike, v: NodeLike, w: float = 1.0) -> None:
        if w == 0:
            return
        self.adj.setdefault(u, {})
        self.adj.setdefault(v, {})
        if u == v:
            self.adj[u][u] = self.adj[u].get(u, 0.0) + w
            return
        self.adj[u][v] = self.adj[u].get(v, 0.0) + w
        self.adj[v][u] = self.adj[v].get(u, 0.0) + w

    def neighbors(self, u: NodeLike) -> Iterable[NodeLike]:
        return self.adj.get(u, {}).keys()

    def weight(self, u: NodeLike, v: NodeLike) -> float:
        return self.adj.get(u, {}).get(v, 0.0)

    def degree(self, u: NodeLike) -> float:
        return sum(self.adj.get(u, {}).values())

    # E(A, B): total edge weight between (disjoint) sets A and B
    def cut_weight(self, A: Iterable[NodeLike], B: Iterable[NodeLike]) -> float:
        Aset, Bset = set(A), set(B)
        if not Aset or not Bset:
            return 0.0
        w = 0.0
        for a in Aset:
            for b, wb in self.adj.get(a, {}).items():
                if b in Bset:
                    w += wb
        return w
    
    # ||S||: volume of S = sum of degrees in S
    def volume(self, S: Iterable[NodeLike]) -> float:
        return sum(self.degree(u) for u in S)