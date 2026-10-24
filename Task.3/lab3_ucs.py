"""Lab 3 Task 3: Uniform-Cost Search on a weighted A-G graph.

IMPORTANT: The assignment's exact Section 3.7 graph/weights were not included
in the screenshot. These weights and the extra corridor are illustrative.
Replace WEIGHTED_GRAPH with the exact lab-manual topology and edge weights.
"""

import heapq
from itertools import count

# Undirected weighted example; every edge weight is stated explicitly.
WEIGHTED_GRAPH = {
    "A": {"B": 2, "C": 5},
    "B": {"A": 2, "D": 4, "E": 7},
    "C": {"A": 5, "F": 2},
    "D": {"B": 4},
    "E": {"B": 7, "G": 2},
    "F": {"C": 2, "G": 6},
    "G": {"E": 2, "F": 6},
}
START = "A"
GOAL = "G"


def ucs(graph, start, goal):
    sequence = count()
    frontier = [(0, next(sequence), start)]
    best_cost = {start: 0}
    parent = {start: None}
    settled = set()
    processing_order = []
    trace = []

    while frontier:
        cost, _, node = heapq.heappop(frontier)

        if node in settled:
            continue
        if cost != best_cost.get(node):
            continue

        settled.add(node)
        processing_order.append(node)
        trace.append((node, cost, sorted(
            (entry_cost, entry_node)
            for entry_cost, _, entry_node in frontier
            if entry_node not in settled
        )))

        # Goal is accepted when removed from the priority queue at minimum cost.
        if node == goal:
            break

        for neighbor, weight in graph.get(node, {}).items():
            if weight < 0:
                raise ValueError("UCS requires non-negative edge weights")
            new_cost = cost + weight
            if neighbor not in settled and new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(frontier, (new_cost, next(sequence), neighbor))

    if goal not in best_cost:
        return [], float("inf"), processing_order, trace

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, best_cost[goal], processing_order, trace


def path_cost(graph, path):
    total = 0
    for a, b in zip(path, path[1:]):
        if b not in graph.get(a, {}):
            raise ValueError(f"Missing edge {a}-{b}")
        total += graph[a][b]
    return total


def bfs_path(graph, start, goal):
    """BFS route on the same topology, ignoring weights."""
    from collections import deque
    queue = deque([start])
    parent = {start: None}
    seen = {start}

    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for neighbor in graph.get(node, {}):
            if neighbor not in seen:
                seen.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

    if goal not in parent:
        return []
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


if __name__ == "__main__":
    print("WEIGHTED EDGES")
    seen_edges = set()
    for node, neighbors in WEIGHTED_GRAPH.items():
        for neighbor, weight in neighbors.items():
            edge = tuple(sorted((node, neighbor)))
            if edge not in seen_edges:
                seen_edges.add(edge)
                print(f"{edge[0]} -- {edge[1]}: {weight}")

    path, cost, order, trace = ucs(WEIGHTED_GRAPH, START, GOAL)
    print("\nUCS processing order:", " -> ".join(order))
    print("UCS path:", " -> ".join(path) if path else "No path")
    print("UCS returned cost:", cost)
    print("UCS independently summed cost:", path_cost(WEIGHTED_GRAPH, path) if path else "N/A")
    print("UCS trace (processed node, cumulative cost, queued frontier):")
    for node, node_cost, frontier in trace:
        print(f"  {node}, cost={node_cost}, frontier={frontier}")

    route = bfs_path(WEIGHTED_GRAPH, START, GOAL)
    print("\nBFS route on same topology:", " -> ".join(route) if route else "No path")
    print("BFS route hop count:", len(route) - 1 if route else "N/A")
    print("BFS route weighted cost:", path_cost(WEIGHTED_GRAPH, route) if route else "N/A")
    print("\nInterpretation: BFS minimizes number of edges, not total edge weight.")
    print("UCS minimizes total cost when all edge weights are non-negative.")
