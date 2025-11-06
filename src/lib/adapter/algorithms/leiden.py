from __future__ import annotations
"""
File: src/lib/adapter/algorithms/leiden.py
Adapter: Leiden via the shared kernel (phase_1/01), plus phase_1/03 enhancements:
- detect_many: resolution scan over gammas, K seeds, Pareto frontier, consensus.
- Optional theta schedule and early-stop plateau.
"""
from typing import Optional, List, Set, Dict, Any
from itertools import combinations

from src.lib.port.algorithms.CommunityDetection import CommunityDetectionPort
from src.lib.port.algorithms.Kernel import KernelPort
from src.lib.port.objective import ObjectivePort
from src.lib.domain.types.nodes import BaseNode
from src.lib.domain.types.delta import DeltaFn
from src.lib.domain.models.graph import Graph
from src.lib.domain.models.partition import Partition
from src.lib.domain.services.partition import singleton_partition
from src.lib.adapter.algorithms.kernel import SharedKernel
from src.lib.adapter.objectives.modularity import ModularityObjective

class LeidenAdapter(CommunityDetectionPort):
    def __init__(self, kernel: Optional[KernelPort] = None) -> None:
        self._kernel = kernel or SharedKernel(seed=42)

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
        p_final = self._kernel.multi_level(
            g, p, delta_fn=delta_fn, gamma=gamma, theta=theta, max_levels=max_levels
        )
        return p_final.flattened_partition()

    # --- phase_1/03 additions ---
    def detect_many(
        self,
        g: Graph,
        p0: Optional[Partition],
        *,
        objectives: List[ObjectivePort],
        gammas: List[float],
        seeds: int = 8,
        theta_schedule: Optional[List[float]] = None,
        levels_per_stage: int = 1,
        plateau_eps: float = 1e-9,
        plateau_patience: int = 2,
    ) -> Dict[str, Any]:
        """
        Resolution scan + consensus.
        Returns:
          {
            "runs": [
              {"objective": name, "gamma": γ, "seed": k, "num_communities": m, "score": s, "communities": [...]}
            ],
            "frontier": [{"objective": name, "gamma": γ, "num_communities": m, "score": s}],
            "consensus": [{"objective": name, "gamma": γ, "communities": [...]}],
          }
        """
        theta_schedule = theta_schedule or [1.0, 0.5, 0.25]
        base_p = p0 or singleton_partition(g)

        all_runs: List[Dict[str, Any]] = []
        consensus_out: List[Dict[str, Any]] = []

        for obj in objectives:
            for gamma in (gammas or [1.0]):
                # If objective supports resolution parameterization, refresh it
                active_obj = obj
                if hasattr(obj, "with_gamma") and callable(getattr(obj, "with_gamma")):
                    try:
                        active_obj = obj.with_gamma(gamma)  # type: ignore[attr-defined]
                    except Exception:
                        active_obj = obj  # fallback: ignore gamma

                for seed in range(seeds):
                    kernel = SharedKernel(seed=seed)
                    delta = active_obj.delta_fn(g, base_p)

                    # staged refinement with theta schedule + early stop
                    p_stage = base_p
                    best_s = float("-inf")
                    no_improve = 0

                    for t in theta_schedule:
                        p_stage = kernel.multi_level(
                            g,
                            p_stage,
                            delta_fn=delta,
                            gamma=gamma,
                            theta=t,
                            max_levels=levels_per_stage,
                        )
                        s_now = active_obj.score(g, p_stage)
                        if s_now <= best_s + plateau_eps:
                            no_improve += 1
                            if no_improve >= plateau_patience:
                                break
                        else:
                            best_s = s_now
                            no_improve = 0

                    comms = p_stage.flattened_partition()
                    all_runs.append({
                        "objective": type(active_obj).__name__,
                        "gamma": float(gamma),
                        "seed": int(seed),
                        "num_communities": len(comms),
                        "score": active_obj.score(g, p_stage),
                        "communities": comms,
                    })

                # --- consensus across seeds for this (objective, gamma) ---
                seed_partitions = [r for r in all_runs
                                   if r["objective"] == type(active_obj).__name__ and r["gamma"] == float(gamma)]
                if seed_partitions:
                    cons_comms = self._consensus_recluster(g, seed_partitions)
                    consensus_out.append({
                        "objective": type(active_obj).__name__,
                        "gamma": float(gamma),
                        "communities": cons_comms,
                    })

        frontier = self._pareto_frontier(all_runs)
        return {"runs": all_runs, "frontier": frontier, "consensus": consensus_out}

    # --- helpers ---
    def _pareto_frontier(self, runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Pareto over (score ↑, num_communities ↓) per (objective, gamma) best-of-seeds.
        """
        best_per = {}
        for r in runs:
            key = (r["objective"], r["gamma"])
            if key not in best_per or r["score"] > best_per[key]["score"]:
                best_per[key] = r

        points = list(best_per.values())
        # non-dominated filter: keep r if not dominated by any q
        out: List[Dict[str, Any]] = []
        for r in points:
            dominated = False
            for q in points:
                if q is r:
                    continue
                if (q["score"] >= r["score"] and q["num_communities"] <= r["num_communities"]
                        and (q["score"] > r["score"] or q["num_communities"] < r["num_communities"])):
                    dominated = True
                    break
            if not dominated:
                out.append({
                    "objective": r["objective"],
                    "gamma": r["gamma"],
                    "num_communities": r["num_communities"],
                    "score": r["score"],
                })
        # sort for readability
        out.sort(key=lambda x: (x["objective"], x["gamma"]))
        return out

    def _consensus_recluster(self, g: Graph, seed_runs: List[Dict[str, Any]]) -> List[Set[BaseNode]]:
        """
        Build a co-association graph from multiple seed partitions and recluster it.
        We recluster with modularity on the co-association graph for stability.
        """
        # collect base nodes from the original graph
        base_nodes = list(g.nodes())  # assuming base nodes; if supernodes, caller should expand earlier
        idx = {n: i for i, n in enumerate(base_nodes)}
        n = len(base_nodes)
        if n == 0:
            return []

        # co-association counts
        counts = [[0.0] * n for _ in range(n)]
        num_partitions = len(seed_runs)

        for run in seed_runs:
            for comm in run["communities"]:  # flattened sets of BaseNode
                comm_list = [x for x in comm if x in idx]
                for a, b in combinations(comm_list, 2):
                    ia, ib = idx[a], idx[b]
                    counts[ia][ib] += 1.0
                    counts[ib][ia] += 1.0

        # normalize to [0,1] by number of partitions
        norm = float(max(num_partitions, 1))
        # build co-association graph
        Gc = Graph()
        for i in range(n):
            for j in range(i + 1, n):
                w = counts[i][j] / norm
                if w > 0.0:
                    Gc.add_edge(base_nodes[i], base_nodes[j], w)

        # recluster with modularity
        mod = ModularityObjective()
        kernel = SharedKernel(seed=1234)
        delta = mod.delta_fn(Gc, singleton_partition(Gc))
        p_final = kernel.multi_level(Gc, singleton_partition(Gc), delta_fn=delta, gamma=1.0, theta=1.0, max_levels=100)
        return p_final.flattened_partition()
