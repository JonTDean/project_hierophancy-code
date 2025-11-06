## Appendix B — Cross-Cutting Notes

* **Supernodes**: All new code must accept `NodeLike` (base or frozenset). Visualizers should expand labels for supernodes or show centroids.
* **Determinism**: All randomized logic must accept a seed; default to `7` for parity with `RandomLayout`.
* **Performance**: Prefer dictionary iteration patterns already used; avoid double‑counting undirected edges (see `aggregate_graph`).
* **Type fidelity**: Keep `DeltaFn` signature; layer `ObjectivePort` on top without breaking callers.
