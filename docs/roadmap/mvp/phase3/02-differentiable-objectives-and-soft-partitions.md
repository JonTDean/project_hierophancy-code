# Differentiable Objectives & Soft Partitions

## Idea
Relax discrete partitions to soft assignments S in R^{n x k} with row-wise simplex constraints. Optimize smooth surrogates of modularity or CPM via gradient methods.

## Pieces
- Soft modularity: maximize trace(S^T B S), where B is the modularity matrix.
- Constraints: row-softmax or Sinkhorn normalization.
- Gumbel-Softmax for near-discrete samples (temperature schedule).

## API
- Loss builders that take Graph and produce differentiable losses.
- Hooks to compare with hard partitions via argmax and ARI/NMI.
