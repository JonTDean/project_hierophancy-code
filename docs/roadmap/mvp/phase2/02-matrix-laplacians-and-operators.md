# Laplacians & Graph Operators

## Goal
Standardize construction of graph operators for spectral/diffusion methods.

## API (new)
- `LaplacianPort`:
  ```python
  class LaplacianPort(Protocol):
      def degrees(self, G: Graph) -> dict[NodeLike, float]: ...
      def adjacency(self, G: Graph) -> dict[NodeLike, dict[NodeLike, float]]: ...
      def laplacians(self, G: Graph, *, normalized: bool = True) -> tuple[NDArray, NDArray, NDArray]:
          """Returns (L, L_rw, L_sym) in a reproducible node order."""
  ```

## Design Notes
- Treat self‑loops as degree contributions.
- Preserve symmetry: `adj[u][v] == adj[v][u]`.
- Deterministic node ordering for matrix builds; expose index map.

## Caching
- Hash graph by `(num_nodes, num_edges, sum(weights), seed)`; cache L and eigenpairs where feasible.

## Acceptance
- Symmetry within 1e-12; PSD check for normalized Laplacians; unit tests on toy graphs.
