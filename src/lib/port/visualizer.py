from __future__ import annotations
from typing import Protocol, Optional, List, Set
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.types.positions import Positions
from src.lib.domain.models.graph import Graph

class VisualizerPort(Protocol):
    def render(
        self,
        G: Graph,
        final_partition: List[Set[NodeLike]],
        positions: Positions,
        title: str = "Graph edges and convex hulls per community",
        save_path: Optional[str] = None,
    ) -> Optional[str]: ...
