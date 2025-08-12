import matplotlib.pyplot as plt
import networkx as nx
import time

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

def draw_graph(assignments, step):
    plt.clf()
    G = nx.Graph(graph)
    node_colors = [assignments.get(node, 'white') for node in G.nodes()]
    nx.draw(G, pos=positions, with_labels=True, node_color=node_colors, node_size=1500, font_size=10)
    plt.title(f"Forward Checking Step {step}")
    plt.pause(0.8)

def forward_checking(assignments, domains, step=0):
    if len(assignments) == len(graph):
        draw_graph(assignments, step)
        return assignments

    unassigned = [n for n in graph if n not in assignments][0]
    for color in domains[unassigned][:]:
        local_domains = {var: list(domains[var]) for var in domains}
        assignments[unassigned] = color

        # Remove this color from neighbors' domains
        for neighbor in graph[unassigned]:
            if color in local_domains[neighbor]:
                local_domains[neighbor].remove(color)

        draw_graph(assignments, step)

        if all(local_domains[v] for v in graph if v not in assignments):
            result = forward_checking(assignments, local_domains, step + 1)
            if result:
                return result

        del assignments[unassigned]
    return None

domains = {var: list(colors) for var in graph}
plt.figure(figsize=(6, 4))
solution = forward_checking({}, domains)
plt.show()
print("✅ Solution:", solution)
