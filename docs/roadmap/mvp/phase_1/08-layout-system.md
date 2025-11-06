# docs/roadmap/08-layout-system.md

## Goal

Offer multiple deterministic layouts with caching and consistent scaling.

## Layouts

* `FruchtermanReingoldLayout(seed)`
* `SpectralLayout()` using eigenvectors of L (if available)
* `ForceAtlas2Layout(seed)` (approximate)
* `Grid/HierarchicalLayout` for aggregated graphs across levels

## API

* Keep `LayoutPort`; add `LayoutCache`:

  ```python
  class LayoutCache(Protocol):
      def get(self, g_hash: str, key: str) -> Positions | None: ...
      def put(self, g_hash: str, key: str, pos: Positions) -> None: ...
  ```

## Acceptance Criteria

* Same seed ⇒ same coordinates.
* Aggregated graphs inherit positions by supernode centroids when possible.