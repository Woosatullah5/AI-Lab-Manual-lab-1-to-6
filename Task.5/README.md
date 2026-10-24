# Lab 5 — Minimax and Alpha-Beta Pruning

## Included
- `lab5_minimax.py`: minimax, alpha-beta pruning, terminal-leaf counters, branch reordering, and comparison output.

## Run
Requires Python 3; no third-party packages:
```bash
python lab5_minimax.py
```

## Important graph/tree note
The uploaded screenshot includes the task instructions but does not show the supplied game tree or leaf values. The script therefore uses a clearly labelled illustrative tree. Replace `TREE` with the exact tree from the lab manual before submission. Keep the root player and MAX/MIN level convention consistent with the supplied tree.

## Counting convention
The leaf counter increments only when a terminal utility value is evaluated. Internal nodes are not counted as leaves. The goal of the comparison is to show that minimax and alpha-beta agree on the root value while alpha-beta's leaf count can change with branch ordering.
