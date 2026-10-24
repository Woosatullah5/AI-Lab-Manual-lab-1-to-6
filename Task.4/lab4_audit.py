"""Lab 4: Heuristic audit for the example graph."""

from lab4_astar import GRAPH, HEURISTIC, GOAL


def shortest_costs_to_goal(graph, goal):
    # Reverse-graph Dijkstra, used to independently calculate true remaining costs.
    import heapq
    reverse = {node: {} for node in graph}
    for u, neighbors in graph.items():
        for v, weight in neighbors.items():
            reverse[v][u] = weight

    costs = {goal: 0}
    queue = [(0, goal)]
    while queue:
        cost, node = heapq.heappop(queue)
        if cost != costs[node]:
            continue
        for prev, weight in reverse[node].items():
            new_cost = cost + weight
            if new_cost < costs.get(prev, float("inf")):
                costs[prev] = new_cost
                heapq.heappush(queue, (new_cost, prev))
    return costs


if __name__ == "__main__":
    true_costs = shortest_costs_to_goal(GRAPH, GOAL)
    print("Heuristic audit (illustrative graph)")
    print("Node | h(n) | true remaining cost | admissible?")
    for node in GRAPH:
        h = HEURISTIC.get(node, 0)
        true_cost = true_costs.get(node, float("inf"))
        print(f"{node:>4} | {h:>4} | {true_cost:>19} | {h <= true_cost}")
