"""Lab 3 Task 2: Depth-Limited Search (DLS) and IDDFS.

IMPORTANT: GRAPH is an illustrative placeholder because the original
Section 3.2 graph was not present in the supplied screenshot. Replace it
with the exact graph and successor order from the lab manual.
The root is counted at depth 0.
"""

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B"],
    "E": ["B", "G"],
    "F": ["C", "G"],
    "G": ["E", "F"],
}
START = "A"
GOAL = "G"


def dls(graph, start, goal, limit):
    """Return (status, path, visit_order, trace), status in FOUND/CUTOFF/FAILURE."""
    visit_order = []
    trace = []
    cutoff_occurred = False

    def visit(node, depth, path):
        nonlocal cutoff_occurred
        visit_order.append(node)
        trace.append((node, depth, list(path)))

        # Goal test happens when the node is processed.
        if node == goal:
            return "FOUND", list(path)

        if depth == limit:
            if graph.get(node, []):
                cutoff_occurred = True
            return "CUTOFF" if cutoff_occurred else "FAILURE", []

        saw_cutoff = False
        for successor in graph.get(node, []):
            if successor in path:
                continue
            status, found_path = visit(successor, depth + 1, path + [successor])
            if status == "FOUND":
                return status, found_path
            if status == "CUTOFF":
                saw_cutoff = True

        if saw_cutoff:
            return "CUTOFF", []
        return "FAILURE", []

    status, path = visit(start, 0, [start])
    return status, path, visit_order, trace


def iddfs(graph, start, goal, max_depth):
    attempts = []
    for limit in range(max_depth + 1):
        status, path, visit_order, trace = dls(graph, start, goal, limit)
        attempts.append({
            "limit": limit,
            "status": status,
            "path": path,
            "visit_order": visit_order,
            "trace": trace,
        })
        if status == "FOUND":
            break
    return attempts


if __name__ == "__main__":
    print("DLS at limits 1, 2, 3, and 4")
    for limit in [1, 2, 3, 4]:
        status, path, order, trace = dls(GRAPH, START, GOAL, limit)
        print(f"\nLimit={limit} | status={status}")
        print("Processed nodes (node@depth):", " -> ".join(f"{n}@{d}" for n, d, _ in trace))
        print("Path:", " -> ".join(path) if path else "None")

    print("\nIDDFS with maximum depths 1, 2, 3, and 4")
    attempts = iddfs(GRAPH, START, GOAL, 4)
    for attempt in attempts:
        path = " -> ".join(attempt["path"]) if attempt["path"] else "None"
        print(
            f"Limit={attempt['limit']} | status={attempt['status']} | "
            f"path={path} | visit order={' -> '.join(attempt['visit_order'])}"
        )
    print("Limits attempted:", [a["limit"] for a in attempts])
