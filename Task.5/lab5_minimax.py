"""Lab task: Minimax, alpha-beta pruning, leaf counters, and branch ordering.

The uploaded screenshot does not show the supplied game tree or leaf utilities.
This file uses a clearly labelled illustrative complete binary tree. Replace
TREE with the exact tree from the lab manual before submitting.

Convention: root is MAX; levels alternate MAX/MIN; leaf values are numeric.
The counter counts terminal leaf evaluations only, not internal nodes.
"""

from copy import deepcopy

# Illustrative tree:
#                 MAX
#             /         \
#           MIN         MIN
#          /   \       /   \
#        MAX   MAX   MAX   MAX
#       / \   / \   / \   / \
#      3   5 6   9 1   2 0  -1
TREE = [
    [[3, 5], [6, 9]],
    [[1, 2], [0, -1]],
]


def minimax(node, maximizing, counter):
    """Return (value, trace); increments counter['leaves'] at terminal leaves."""
    if not isinstance(node, list):
        counter["leaves"] += 1
        return node, [{"event": "leaf", "value": node}]

    values = []
    trace = []
    for index, child in enumerate(node):
        value, child_trace = minimax(child, not maximizing, counter)
        values.append(value)
        trace.extend(child_trace)
        trace.append({
            "event": "child-return",
            "parent_type": "MAX" if maximizing else "MIN",
            "child_index": index,
            "value": value,
        })

    result = max(values) if maximizing else min(values)
    trace.append({
        "event": "node-return",
        "node_type": "MAX" if maximizing else "MIN",
        "child_values": values,
        "value": result,
    })
    return result, trace


def alpha_beta(node, alpha=float("-inf"), beta=float("inf"), maximizing=True, counter=None):
    """Return (value, trace); terminal leaf counter is shared by reference."""
    if counter is None:
        counter = {"leaves": 0}

    if not isinstance(node, list):
        counter["leaves"] += 1
        return node, [{"event": "leaf", "value": node}]

    trace = []
    if maximizing:
        value = float("-inf")
        for index, child in enumerate(node):
            child_value, child_trace = alpha_beta(
                child, alpha, beta, False, counter
            )
            trace.extend(child_trace)
            value = max(value, child_value)
            alpha = max(alpha, value)
            trace.append({
                "event": "update",
                "node_type": "MAX",
                "child_index": index,
                "value": value,
                "alpha": alpha,
                "beta": beta,
            })
            if alpha >= beta:
                trace.append({
                    "event": "prune",
                    "node_type": "MAX",
                    "next_child_index": index + 1,
                    "alpha": alpha,
                    "beta": beta,
                })
                break
    else:
        value = float("inf")
        for index, child in enumerate(node):
            child_value, child_trace = alpha_beta(
                child, alpha, beta, True, counter
            )
            trace.extend(child_trace)
            value = min(value, child_value)
            beta = min(beta, value)
            trace.append({
                "event": "update",
                "node_type": "MIN",
                "child_index": index,
                "value": value,
                "alpha": alpha,
                "beta": beta,
            })
            if alpha >= beta:
                trace.append({
                    "event": "prune",
                    "node_type": "MIN",
                    "next_child_index": index + 1,
                    "alpha": alpha,
                    "beta": beta,
                })
                break

    trace.append({
        "event": "node-return",
        "node_type": "MAX" if maximizing else "MIN",
        "value": value,
    })
    return value, trace


def reorder_for_example(tree):
    """Reverse child order at each internal node to demonstrate order effects."""
    if not isinstance(tree, list):
        return tree
    return [reorder_for_example(child) for child in reversed(tree)]


def summarize(label, tree):
    mm_counter = {"leaves": 0}
    mm_value, _ = minimax(tree, True, mm_counter)

    ab_counter = {"leaves": 0}
    ab_value, ab_trace = alpha_beta(tree, counter=ab_counter, maximizing=True)
    prune_events = [item for item in ab_trace if item["event"] == "prune"]

    print(f"\n{label}")
    print("-" * len(label))
    print("Tree:", tree)
    print(f"Minimax root value: {mm_value}")
    print(f"Minimax leaf evaluations: {mm_counter['leaves']}")
    print(f"Alpha-beta root value: {ab_value}")
    print(f"Alpha-beta leaf evaluations: {ab_counter['leaves']}")
    print(f"Leaves avoided by alpha-beta: {mm_counter['leaves'] - ab_counter['leaves']}")
    print(f"Pruning events: {len(prune_events)}")
    print("Root values agree:", mm_value == ab_value)
    return mm_value, mm_counter["leaves"], ab_value, ab_counter["leaves"]


if __name__ == "__main__":
    print("NOTE: Illustrative tree only. Replace TREE with the supplied lab tree.")
    original = deepcopy(TREE)
    reordered = reorder_for_example(original)

    first = summarize("ORIGINAL BRANCH ORDER", original)
    second = summarize("REVERSED BRANCH ORDER", reordered)

    print("\nCOMPARISON")
    print("Minimax value unchanged:", first[0] == second[0])
    print("Alpha-beta value unchanged:", first[2] == second[2])
    print("Alpha-beta leaf count changed:", first[3] != second[3])
    print("\nInterpretation:")
    print("- Minimax and alpha-beta must return the same root value on a complete tree.")
    print("- Alpha-beta may evaluate fewer leaves by pruning branches that cannot affect the decision.")
    print("- Branch ordering can change the amount of pruning, but not the minimax value.")
