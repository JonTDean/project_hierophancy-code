from __future__ import annotations
from typing import Tuple, Dict
from src.lib.domain.types.nodes import NodeLike

Position = Tuple[float, float]
Positions = Dict[NodeLike, Position]

Adjacency = Dict[NodeLike, Dict[NodeLike, float]]
