import matplotlib.pyplot as plt
import networkx as nx
import time

# Map Coloring Problem Graph (Australian map example)
graph = {
    'WA': ['NT', 'SA'],
    'NT': ['WA', 'SA', 'Q'],
    'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
    'Q': ['NT', 'SA', 'NSW'],
    'NSW': ['Q', 'SA', 'V'],
    'V': ['SA', 'NSW'],
    'T': []
}

colors = ['red', 'green', 'blue', 'yellow']
positions = {
    'WA': (0, 1),
    'NT': (1, 2),
    'SA': (1, 1),
    'Q': (2, 2),
    'NSW': (2, 1),
    'V': (2, 0),
    'T': (3, 0)
}

# Draw graph with current color assignment
def draw_graph(assignments, step):
    plt.clf()
    G = nx.Graph(graph)
    node_colors = [assignments.get(node, 'white') for node in G.nodes()]
    nx.draw(G, pos=positions, with_labels=True, node_color=node_colors, node_size=1500, font_size=10)
    plt.title(f"Backtracking Step {step}")
    plt.pause(0.8)

# Check if color assignment is valid
def is_valid(node, color, assignments):
    for neighbor in graph[node]:
        if assignments.get(neighbor) == color:
            return False
    return True

# Backtracking CSP Solver
def backtrack(assignments, step=0):
    if len(assignments) == len(graph):
        draw_graph(assignments, step)
        return assignments
    
    unassigned = [n for n in graph if n not in assignments][0]
    for color in colors:
        if is_valid(unassigned, color, assignments):
            assignments[unassigned] = color
            draw_graph(assignments, step)
            result = backtrack(assignments, step + 1)
            if result:
                return result
            del assignments[unassigned]
    return None

plt.figure(figsize=(6, 4))
solution = backtrack({})
plt.show()
print("✅ Solution:", solution)
