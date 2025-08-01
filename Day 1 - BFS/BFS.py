import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

# Define the Graph
graph = {
    'A': ['B', 'C', 'F'],
    'B': ['D', 'E'],
    'C': ['F', 'E'],
    'D': ['C', 'A'],
    'E': ['G', 'A'],
    'F': ['D', 'E', 'B', 'G'],
    'G': ['D', 'B', 'C']
}

def bfs_visualize_all(graph, start, goal):
    visited = set()
    queue = deque([[start]])
    explored_edges = []
    visited_nodes = []

    G = nx.DiGraph()
    for node in graph:
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G, seed=42)

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            visited.add(node)
            visited_nodes.append(node)

            # === New Figure for Each Step ===
            fig, ax = plt.subplots(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color='skyblue',
                    edge_color='gray', node_size=1800, font_size=14, ax=ax)

            nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color='lightgreen', node_size=2000, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=explored_edges, edge_color='orange', width=2, ax=ax)

            ax.set_title(f"Searching: {node}", fontsize=18)
            plt.tight_layout()
            plt.show()  # Waits until window is closed

            if node == goal:
                path_edges = list(zip(path, path[1:]))
                fig, ax = plt.subplots(figsize=(8, 6))
                nx.draw(G, pos, with_labels=True, node_color='skyblue',
                        edge_color='gray', node_size=1800, font_size=14, ax=ax)
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lime', node_size=2200, ax=ax)
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
                ax.set_title(f" Final Path: {' -> '.join(path)}", fontsize=16)
                plt.tight_layout()
                plt.show()
                return path

            for neighbor in graph[node]:
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    explored_edges.append((node, neighbor))

    print(" Goal Not Found")
    return None

# Run Visualization
start = 'A'
goal = 'G'
final_path = bfs_visualize_all(graph, start, goal)

if final_path:
    print("✅ Final Path:", " -> ".join(final_path))
else:
    print(" No Path Found")
