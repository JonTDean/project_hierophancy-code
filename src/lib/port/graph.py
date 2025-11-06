from __future__ import annotations
from typing import Protocol, Sequence, Tuple
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.models.graph import Graph

class GraphBuilderPort(Protocol):
    def build(self, edges: Sequence[Tuple[NodeLike, NodeLike, float]]) -> Graph: ...
