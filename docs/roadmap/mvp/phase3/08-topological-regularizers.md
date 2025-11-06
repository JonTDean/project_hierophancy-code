# Topological Regularizers

## Idea
Encourage embeddings that preserve salient topology using persistence-based penalties.

## Plan
- Compute persistence on batches; penalize loss of long-lived features, or encourage desired holes/loops.
- Stability checks across seeds and training epochs.
