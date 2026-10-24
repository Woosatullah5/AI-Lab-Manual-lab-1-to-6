# Lab 4 - A* and UCS

## Files
- `lab4_astar.py`: A* search, zero-heuristic UCS control, processed-node trace, path costs, expansion counts, and one-value heuristic overestimate experiment.
- `lab4_audit.py`: heuristic audit comparing h(n) with independently computed true remaining costs.
- `README.md`: run commands and assumptions.

## Run (Python 3, no third-party packages)
```bash
python lab4_audit.py
python lab4_astar.py
```

## Important
The screenshot includes task instructions but not the supplied campus graph or heuristic table. The graph and heuristic in these files are an illustrative example only. Before submission, replace `GRAPH` and `HEURISTIC` in `lab4_astar.py` with the exact manual values, then rerun both scripts and update report tables from the actual output. The overestimate experiment changes only h(A), from 5 to 100.
