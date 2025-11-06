from __future__ import annotations
"""
File: src/lib/adapter/algorithms/kernel.py
Adapter: Concrete shared kernel that wires domain services into a deterministic,
instrumented execution core (move/refine/aggregate/multi_level).
Status: 🔄 WIP
"""
import time
import random
from contextlib import contextmanager
from typing import Optional, Tuple, Callable

from src.lib.port.algorithms.Kernel import KernelPort, KernelEvents, ProgressCallback
from src.lib.domain.types.delta import DeltaFn
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.services.graph import move_nodes_fast, aggregate_graph
from src.lib.domain.services.partition import refine_partition, lift_partition_to_aggregated
from src.lib.domain.services import kernel_invariants as ki

class SharedKernel(KernelPort):
    def __init__(self, *, seed: int = 0, on_event: Optional[ProgressCallback] = None) -> None:
        self._rng = random.Random(seed)
        self._seed = seed
        self._on_event = on_event
        self._t_cumulative = 0.0

    # --- RNG control: all domain randomness flows through here ---
    @contextmanager
    def _global_rng(self):
        prev_state = random.getstate()
        random.setstate(self._rng.getstate())
        try:
            yield
        finally:
            # capture advanced state back into the kernel RNG and restore caller RNG
            self._rng.setstate(random.getstate())
            random.setstate(prev_state)

    # --- delta wrapper to measure attempts and positive deltas ---
    def _wrap_delta(self, delta_fn: DeltaFn) -> Tuple[DeltaFn, Callable[[], Tuple[int, int]]]:
        tried = 0
        positive = 0

        def wrapped(g: Graph, p: Partition, v, dest) -> float:
            nonlocal tried, positive
            tried += 1
            val = delta_fn(g, p, v, dest)
            if val > 0:
                positive += 1
            return val

        def counters() -> Tuple[int, int]:
            return tried, positive

        return wrapped, counters

    def _emit(self, ev: KernelEvents) -> None:
        if self._on_event:
            self._on_event(ev)

    # --- building blocks ---
    def local_move(self, g: Graph, p: Partition, delta_fn: DeltaFn) -> Partition:
        ki.validate(g, p)
        wrapped, ctrs = self._wrap_delta(delta_fn)
        before = dict(p.node2com)

        t0 = time.perf_counter()
        with self._global_rng():
            p2 = move_nodes_fast(g, p, wrapped)
        dt = time.perf_counter() - t0
        self._t_cumulative += dt

        # approximate #moves by final membership changes
        moves_applied = sum(1 for n, c in p2.node2com.items() if before.get(n) != c)
        tried, positive = ctrs()

        self._emit(KernelEvents(
            phase="local_move",
            level_index=-1,  # filled by multi_level
            moves_tried=tried,
            moves_applied=moves_applied,
            deltas_positive=positive,
            seconds_phase=dt,
            cumulative_seconds=self._t_cumulative,
            communities=p2.size(),
            nodes=len(g.nodes()),
            seed=self._seed,
        ))
        ki.validate(g, p2)
        return p2

    def refine(
        self,
        g: Graph,
        p: Partition,
        *,
        delta_fn: DeltaFn,
        gamma: float,
        theta: float,
    ) -> Partition:
        ki.validate(g, p)
        wrapped, ctrs = self._wrap_delta(delta_fn)

        t0 = time.perf_counter()
        with self._global_rng():
            pref = refine_partition(g, p, wrapped, gamma, theta)
        dt = time.perf_counter() - t0
        self._t_cumulative += dt

        tried, positive = ctrs()
        self._emit(KernelEvents(
            phase="refine",
            level_index=-1,
            moves_tried=tried,
            moves_applied=0,  # merges happen inside service; not observable here
            deltas_positive=positive,
            seconds_phase=dt,
            cumulative_seconds=self._t_cumulative,
            communities=pref.size(),
            nodes=len(g.nodes()),
            seed=self._seed,
        ))
        ki.validate(g, pref)
        return pref

    def aggregate(self, g: Graph, p_refined: Partition) -> Graph:
        ki.validate(g, p_refined)

        t0 = time.perf_counter()
        with self._global_rng():
            g2 = aggregate_graph(g, p_refined)
        dt = time.perf_counter() - t0
        self._t_cumulative += dt

        self._emit(KernelEvents(
            phase="aggregate",
            level_index=-1,
            seconds_phase=dt,
            cumulative_seconds=self._t_cumulative,
            communities=p_refined.size(),
            nodes=len(g2.nodes()),
            seed=self._seed,
        ))
        # no partition to validate here; validate on next round with lifted p
        return g2

    def multi_level(
        self,
        g: Graph,
        p0: Partition,
        *,
        delta_fn: DeltaFn,
        gamma: float,
        theta: float,
        max_levels: int,
    ) -> Partition:
        ki.validate(g, p0)
        level = 0
        p = p0

        while True:
            # 1) local move
            p = self.local_move(g, p, delta_fn)

            # domain-compat: stop when every node is a singleton community
            done = (p.size() == len(g.nodes()))
            if not done and level < max_levels:
                # 2) refine within each community
                pref = self.refine(g, p, delta_fn=delta_fn, gamma=gamma, theta=theta)
                # 3) aggregate graph + lift partition
                g = self.aggregate(g, pref)
                p = lift_partition_to_aggregated(p, pref)
                level += 1

                self._emit(KernelEvents(
                    phase="level_end",
                    level_index=level,
                    seconds_phase=0.0,
                    cumulative_seconds=self._t_cumulative,
                    communities=p.size(),
                    nodes=len(g.nodes()),
                    seed=self._seed,
                ))
                continue

            # done
            self._emit(KernelEvents(
                phase="done",
                level_index=level,
                seconds_phase=0.0,
                cumulative_seconds=self._t_cumulative,
                communities=p.size(),
                nodes=len(g.nodes()),
                seed=self._seed,
            ))
            ki.validate(g, p)
            return p
