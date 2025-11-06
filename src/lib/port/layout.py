from __future__ import annotations
from typing import Protocol
from src.lib.domain.types.positions import Positions
from src.lib.domain.models.graph import Graph


class LayoutPort(Protocol):
    def get_positions(self, G: Graph) -> Positions: ...