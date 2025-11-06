from __future__ import annotations
import random
from src.lib.domain.models.graph import Graph
from src.lib.domain.types.positions import Positions
from src.lib.port.layout import LayoutPort

class RandomLayout(LayoutPort):
    def __init__(self, seed: int = 7) -> None:
        self._seed = seed

    def get_positions(self, G: Graph) -> Positions:
        rnd = random.Random(self._seed)
        return {n: (rnd.random(), rnd.random()) for n in G.nodes()}
