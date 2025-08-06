import matplotlib.pyplot as plt
import networkx as nx
import heapq
import time

# Define the graph with connections and distances
graph = {
    'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
    'Zerind': {'Oradea': 71, 'Arad': 75},
    'Oradea': {'Sibiu': 151, 'Zerind': 71},
    'Sibiu': {'Fagaras': 99, 'Rimnicu Vilcea': 80, 'Arad': 140, 'Oradea': 151},
    'Fagaras': {'Bucharest': 211, 'Sibiu': 99},
    'Rimnicu Vilcea': {'Pitesti': 97, 'Craiova': 146, 'Sibiu': 80},
    'Pitesti': {'Bucharest': 101, 'Rimnicu Vilcea': 97},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101}
}

# Heuristic (Straight-line distance to Bucharest)
heuristic = {
    'Arad': 366, 'Zerind': 374, 'Oradea': 380, 'Sibiu': 253, 'Fagaras': 176,
    'Rimnicu Vilcea': 193, 'Pitesti': 100, 'Timisoara': 329, 'Lugoj': 244,
    'Mehadia': 241, 'Drobeta': 242, 'Craiova': 160, 'Bucharest': 0
}

# Create Graph Layout
G = nx.Graph()
for city in graph:
    for neighbor in graph[city]:
        G.add_edge(city, neighbor)
pos = nx.spring_layout(G, seed=42)  # fixed layout

# Draw the graph state
def draw_graph(current=None, path=[], final=False):
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=10)

    if current:
        nx.draw_networkx_nodes(G, pos, nodelist=[current], node_color='yellow', node_size=1800)

    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, edge_color='red')

    title = "Final Path" if final else f"Exploring: {current}"
    plt.title(f"Greedy Best First Search - {title}")
    plt.draw()
    plt.pause(1)

# Greedy Best First Search
def greedy_best_first_search(start, goal):
    visited = set()
    queue = [(heuristic[start], start, [start])]

    while queue:
        _, current_node, current_path = heapq.heappop(queue)
        draw_graph(current=current_node, path=current_path)

        if current_node == goal:
            print("✅ Path found:", " -> ".join(current_path))
            return current_path

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic[neighbor], neighbor, current_path + [neighbor]))

    print("❌ No path found.")
    return None

# Run Search
plt.ion()
fig = plt.figure(figsize=(10, 7))
final_path = greedy_best_first_search('Arad', 'Mehadia')
draw_graph(path=final_path, final=True)
plt.ioff()
plt.show()
