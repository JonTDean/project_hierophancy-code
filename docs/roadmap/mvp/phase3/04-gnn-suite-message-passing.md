# GNN Suite — Message Passing

## Models
- GCN, GraphSAGE, GAT, GIN with weighted edges and self-loops.
- Readout heads for node, edge, and community-level predictions.
- Semi-supervised setup with label masks and partition priors.

## Integration
- Use ObjectivePort losses (e.g., soft modularity) as regularizers.
- Compatibility with supernodes from aggregated graphs (pooling-like behavior).
