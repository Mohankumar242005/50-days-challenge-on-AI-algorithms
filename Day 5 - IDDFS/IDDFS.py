import matplotlib.pyplot as plt
import networkx as nx
import time

# === Graph Definition ===
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['G'],
    'E': ['G'],
    'F': ['D', 'G'],
    'G': ['D', 'E'],
}

# === Visualization Setup ===
G = nx.DiGraph()
for node in graph:
    for neighbor in graph[node]:
        G.add_edge(node, neighbor)

pos = nx.spring_layout(G)

def draw_graph(current_node=None, visited=set(), path=[]):
    plt.clf()
    colors = []

    for node in G.nodes():
        if node == current_node:
            colors.append('orange')  # Currently visiting
        elif node in path:
            colors.append('green')  # Final path
        elif node in visited:
            colors.append('lightblue')  # Already visited
        else:
            colors.append('lightgray')  # Unvisited

    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1000, font_weight='bold', arrows=True)
    plt.pause(1)

# === Depth-Limited DFS ===
def depth_limited_dfs(node, goal, limit, visited, path):
    draw_graph(current_node=node, visited=visited, path=path)
    if node == goal:
        return True
    if limit <= 0:
        return False

    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            path.append(neighbor)
            if depth_limited_dfs(neighbor, goal, limit - 1, visited, path):
                return True
            path.pop()
    return False

# === Iterative Deepening DFS ===
def iddfs(start, goal, max_depth):
    for depth in range(max_depth + 1):
        print(f"🔁 Searching at depth limit: {depth}")
        visited = set()
        path = [start]
        if depth_limited_dfs(start, goal, depth, visited, path):
            draw_graph(current_node=None, visited=visited, path=path)
            print("✅ Final Path:", " -> ".join(path))
            return path
    print("❌ Goal not found within depth limit.")
    return []

# === Run the Program ===
plt.ion()
plt.figure(figsize=(8, 6))

start_node = 'A'
goal_node = 'G'
max_depth = 5

iddfs(start_node, goal_node, max_depth)

plt.ioff()
plt.show()
