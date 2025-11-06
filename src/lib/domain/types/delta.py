from __future__ import annotations

from typing import Callable, Optional, TYPE_CHECKING
from src.lib.domain.types.nodes import NodeLike

if TYPE_CHECKING:
    from src.lib.domain.models.graph import Graph
    from src.lib.domain.models.partition import Partition

DeltaFn = Callable[['Graph', 'Partition', NodeLike, Optional[object]], float]
