import heapq
import matplotlib.pyplot as plt
import networkx as nx
import time

# --- Romania Map as Graph ---
romania_map = {
    'A': [('B', 75), ('C', 140)],
    'B': [('D', 71), ('A', 75)],
    'C': [('A', 140), ('D', 99), ('F', 80)],
    'D': [('B', 71), ('C', 99), ('E', 211)],
    'E': [('D', 211), ('F', 101)],
    'F': [('C', 80), ('E', 101), ('G', 90)],
    'G': []  # Goal node
}

# --- Heuristic values (straight-line distance to goal G) ---
heuristic = {
    'A': 366,
    'B': 374,
    'C': 253,
    'D': 178,
    'E': 100,
    'F': 90,
    'G': 0
}

# --- A* Algorithm ---
def a_star_search(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (heuristic[start], 0, start, [start]))
    visited = set()

    G = nx.Graph()
    for city in graph:
        for neighbor, cost in graph[city]:
            G.add_edge(city, neighbor, weight=cost)

    pos = nx.spring_layout(G)

    while open_set:
        est_total_cost, cost_so_far, current, path = heapq.heappop(open_set)
        print(f"Visiting: {current}, Path: {path}, Cost so far: {cost_so_far}")

        if current == goal:
            print(f"✅ Final Path: {' -> '.join(path)}, Cost: {cost_so_far}")
            visualize_path(G, pos, path)
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor, cost in graph[current]:
            if neighbor not in visited:
                total_cost = cost_so_far + cost
                est_cost = total_cost + heuristic[neighbor]
                heapq.heappush(open_set, (est_cost, total_cost, neighbor, path + [neighbor]))

        visualize_path(G, pos, path)
        time.sleep(0.5)

    return None

# --- Visualization ---
def visualize_path(G, pos, path):
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos)
    if len(path) > 1:
        edge_list = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='red', width=2)
    plt.pause(0.5)

# --- Run A* ---
plt.ion()
a_star_search(romania_map, 'A', 'G')
plt.ioff()
plt.show()
