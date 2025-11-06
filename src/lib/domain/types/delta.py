from __future__ import annotations
from typing import Callable, Optional, TYPE_CHECKING
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.types.general import CommunityId

if TYPE_CHECKING:
    from src.lib.domain.models.graph import Graph
    from src.lib.domain.models.partition import Partition

# Delta for moving node v into community 'dest' (or None for a new community)
DeltaFn = Callable[['Graph', 'Partition', NodeLike, Optional[CommunityId]], float]
