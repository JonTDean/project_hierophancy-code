from __future__ import annotations
from typing import Optional, List, Set
from src.lib.port.algorithms.CommunityDetection import CommunityDetectionPort
from src.lib.domain.types.nodes import BaseNode
from src.lib.domain.types.delta import DeltaFn
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.algorithms.distance.leiden import leiden as leiden_domain
from src.lib.domain.services.partition import singleton_partition

class LeidenAdapter(CommunityDetectionPort):
    """
    Adapter: wraps the domain-level Leiden implementation behind the algorithm port.
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
    ) -> List[Set[BaseNode]]:
        p = p0 or singleton_partition(g)
        return leiden_domain(g, p, delta_fn, gamma, theta, max_levels)
