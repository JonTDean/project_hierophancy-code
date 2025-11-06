from __future__ import annotations
from typing import List, Tuple
from src.lib.domain.models.graph import Graph
from src.lib.domain.types.nodes import NodeLike
from src.lib.port.graph import GraphBuilderPort

class EdgesGraphBuilder(GraphBuilderPort):
    def build(self, edges: List[Tuple[NodeLike, NodeLike, float]]) -> Graph:
        G = Graph()
        for u, v, w in edges:
            G.add_edge(u, v, w)
        return G
