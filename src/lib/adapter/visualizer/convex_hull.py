# pyright: reportUnknownMemberType=false

from __future__ import annotations
from typing import Optional, List, Set, FrozenSet

import matplotlib.pyplot as plt

from src.lib.domain.models.graph import Graph
from src.lib.domain.types.nodes import NodeLike
from src.lib.domain.types.positions import Positions, Position
from src.lib.port.visualizer import VisualizerPort

def _cross(o: Position, a: Position, b: Position) -> float:
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def _convex_hull(points: List[Position]) -> List[Position]:
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower: List[Position] = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: List[Position] = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

class MatplotlibVisualizer(VisualizerPort):
    def render(
        self,
        G: Graph,
        final_partition: List[Set[NodeLike]],
        positions: Positions,
        title: str = "Graph edges and convex hulls per community",
        save_path: Optional[str] = None,
    ) -> Optional[str]:
        plt.rcParams["figure.figsize"] = (8.0, 6.0)
        ax = plt.gca()

        drawn: Set[FrozenSet[NodeLike]] = set()
        for u in G.nodes():
            for v in G.neighbors(u):
                key = frozenset((u, v))
                if key in drawn:
                    continue
                drawn.add(key)
                x1, y1 = positions[u]
                x2, y2 = positions[v]
                ax.plot([x1, x2], [y1, y2])

        markers = ['o', 's', '^', 'D', 'P', 'X', '*', 'v', '<', '>']
        for idx, comm in enumerate(final_partition):
            pts: List[Position] = [positions[n] for n in comm]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.scatter(xs, ys, marker=markers[idx % len(markers)], label=f"Community {idx+1}")
            for n in comm:
                x, y = positions[n]
                ax.text(x, y, str(n))
            if len(pts) >= 3:
                hull = _convex_hull(pts)
                if len(hull) >= 3:
                    hx = [p[0] for p in hull] + [hull[0][0]]
                    hy = [p[1] for p in hull] + [hull[0][1]]
                    ax.plot(hx, hy, linewidth=2)

        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend(loc="best")
        ax.set_aspect("equal", adjustable="box")
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=150)
        plt.show()
        return save_path
