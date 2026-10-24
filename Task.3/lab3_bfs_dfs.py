"""Lab 3 Task 1: BFS and DFS trace on an A-G graph.

IMPORTANT: The assignment's original Section 3.2 graph was not included with
the screenshot. The graph below is an illustrative placeholder. Replace GRAPH
with the exact manual graph and successor order before submitting.
Search stops when G is removed from the frontier (goal processing).
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


def reconstruct_path(parent, goal):
    if goal not in parent:
        return []
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return list(reversed(path))


def bfs(graph, start, goal):
    from collections import deque

    frontier = deque([start])
    parent = {start: None}
    discovered = {start}
    visit_order = []
    trace = []

    while frontier:
        node = frontier.popleft()
        visit_order.append(node)
        trace.append({
            "processed": node,
            "frontier": list(frontier),
            "visit_order": list(visit_order),
        })
        if node == goal:
            break

        for successor in graph.get(node, []):
            if successor not in discovered:
                discovered.add(successor)
                parent[successor] = node
                frontier.append(successor)

    return reconstruct_path(parent, goal), visit_order, trace


def dfs(graph, start, goal):
    # Reverse push preserves the listed successor order when using a stack.
    frontier = [start]
    parent = {start: None}
    discovered = {start}
    visit_order = []
    trace = []

    while frontier:
        node = frontier.pop()
        visit_order.append(node)
        trace.append({
            "processed": node,
            "frontier": list(frontier),
            "visit_order": list(visit_order),
        })
        if node == goal:
            break

        for successor in reversed(graph.get(node, [])):
            if successor not in discovered:
                discovered.add(successor)
                parent[successor] = node
                frontier.append(successor)

    return reconstruct_path(parent, goal), visit_order, trace


def print_result(name, result):
    path, visit_order, trace = result
    print(f"\n{name}")
    print("-" * len(name))
    for i, item in enumerate(trace, 1):
        print(
            f"{i}. processed={item['processed']} | "
            f"frontier after expansion/goal check={item['frontier']} | "
            f"visit order={item['visit_order']}"
        )
    print("Final path:", " -> ".join(path) if path else "No path found")
    print("Visit order:", " -> ".join(visit_order))


if __name__ == "__main__":
    print("Graph (replace with the exact Section 3.2 graph):")
    for node, successors in GRAPH.items():
        print(f"  {node}: {successors}")
    print_result("BREADTH-FIRST SEARCH", bfs(GRAPH, START, GOAL))
    print_result("DEPTH-FIRST SEARCH", dfs(GRAPH, START, GOAL))
