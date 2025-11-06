from __future__ import annotations
from typing import Protocol, Optional, List, Set
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.types.nodes import BaseNode
from src.lib.domain.types.delta import DeltaFn

class CommunityDetectionPort(Protocol):
    """
    Port: community-detection algorithm.
    Accepts an optional initial partition; returns final communities as sets of base nodes.
    """
    def detect(
        self,
        g: Graph,
        p0: Optional[Partition],
        *,
        delta_fn: DeltaFn,
        gamma: float = 1.0,
        theta: float = 1.0,
        max_levels: int = 100,
    ) -> List[Set[BaseNode]]: ...
