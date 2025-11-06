from __future__ import annotations
from typing import Hashable, FrozenSet, Union

BaseNode = Hashable
SuperNode = FrozenSet[BaseNode]
NodeLike = Union[BaseNode, SuperNode]