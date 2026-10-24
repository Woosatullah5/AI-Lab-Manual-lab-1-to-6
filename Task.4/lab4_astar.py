"""Lab 4: A* search and UCS control on a small weighted campus graph.

The assignment screenshot does not include the supplied campus graph or heuristic
table. The graph below is a transparent, reproducible example with start S and
goal G. Replace GRAPH and HEURISTIC with the exact lab-manual values before
submitting, and keep successor order consistent.
"""

import heapq
from itertools import count

GRAPH = {
    "S": {"A": 1, "B": 4},
    "A": {"S": 1, "C": 2, "D": 5},
    "B": {"S": 4, "D": 1},
    "C": {"A": 2, "G": 6},
    "D": {"A": 5, "B": 1, "G": 3},
    "G": {"C": 6, "D": 3},
}

# Example heuristic values. h(G) must be 0.
HEURISTIC = {"S": 6, "A": 5, "B": 3, "C": 4, "D": 2, "G": 0}
START = "S"
GOAL = "G"


def reconstruct_path(parent, goal):
    if goal not in parent:
        return []
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def best_first_search(graph, heuristic, start, goal, use_heuristic=True):
    """A* if use_heuristic=True, UCS if False. Tie-breaks by insertion order."""
    sequence = count()
    frontier = [(heuristic.get(start, 0) if use_heuristic else 0, next(sequence), 0, start)]
    best_g = {start: 0}
    parent = {start: None}
    expanded = []
    trace = []
    closed = set()
    stale_entries = 0

    while frontier:
        priority, _, g_at_insert, node = heapq.heappop(frontier)

        # Ignore an outdated queue entry if a cheaper path was found later.
        if g_at_insert != best_g.get(node):
            stale_entries += 1
            trace.append({
                "event": "STALE-SKIP", "node": node, "g": g_at_insert,
                "priority": priority, "frontier": sorted(
                    (p, n, g) for p, _, g, n in frontier
                )
            })
            continue

        # Goal is counted as expanded/processed when popped, consistently in both runs.
        expanded.append(node)
        trace.append({
            "event": "EXPAND", "node": node, "g": g_at_insert,
            "priority": priority, "frontier": sorted(
                (p, n, g) for p, _, g, n in frontier
            )
        })

        if node == goal:
            break

        closed.add(node)
        for neighbor, weight in graph.get(node, {}).items():
            if weight < 0:
                raise ValueError("A* and this UCS implementation require non-negative edge weights")
            tentative_g = g_at_insert + weight
            if tentative_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = tentative_g
                parent[neighbor] = node
                h = heuristic.get(neighbor, 0) if use_heuristic else 0
                f = tentative_g + h
                heapq.heappush(frontier, (f, next(sequence), tentative_g, neighbor))

    path = reconstruct_path(parent, goal)
    cost = best_g.get(goal, float("inf"))
    return {
        "path": path,
        "cost": cost,
        "expanded": expanded,
        "trace": trace,
        "stale_entries_skipped": stale_entries,
    }


def calculate_path_cost(graph, path):
    total = 0
    for u, v in zip(path, path[1:]):
        if v not in graph.get(u, {}):
            raise ValueError(f"Missing edge: {u}-{v}")
        total += graph[u][v]
    return total


def print_result(label, result, graph):
    print(f"\n{label}")
    print("-" * len(label))
    for item in result["trace"]:
        print(
            f"{item['event']}: node={item['node']}, g={item['g']}, "
            f"priority={item['priority']}, frontier={item['frontier']}"
        )
    print("Returned path:", " -> ".join(result["path"]) if result["path"] else "No path")
    print("Returned cost:", result["cost"])
    print("Independent path-cost sum:", calculate_path_cost(graph, result["path"]) if result["path"] else "N/A")
    print("Expanded nodes:", " -> ".join(result["expanded"]))
    print("Expansion count (including goal):", len(result["expanded"]))
    print("Stale entries skipped:", result["stale_entries_skipped"])


if __name__ == "__main__":
    print("Example weighted graph:")
    for u, neighbors in GRAPH.items():
        for v, w in neighbors.items():
            if u < v:
                print(f"{u} -- {v}: {w}")

    astar_result = best_first_search(GRAPH, HEURISTIC, START, GOAL, True)
    ucs_result = best_first_search(GRAPH, HEURISTIC, START, GOAL, False)
    print("\nHeuristic table:", HEURISTIC)
    print_result("A* WITH SUPPLIED EXAMPLE HEURISTIC", astar_result, GRAPH)
    print_result("UCS WITH ZERO HEURISTIC", ucs_result, GRAPH)

    # One heuristic value is changed in Task 3; all other values remain unchanged.
    modified = dict(HEURISTIC)
    modified["A"] = 100
    print("\nOriginal h(A):", HEURISTIC["A"])
    print("Modified h(A):", modified["A"])
    overestimate_result = best_first_search(GRAPH, modified, START, GOAL, True)
    print_result("A* AFTER OVERESTIMATING h(A)", overestimate_result, GRAPH)
