from __future__ import annotations
from typing import Protocol, List, Tuple
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.models.graph import Graph

class GraphBuilderPort(Protocol):
    def build(self, edges: List[Tuple[NodeLike, NodeLike, float]]) -> Graph: ...
