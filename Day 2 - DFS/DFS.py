import matplotlib.pyplot as plt
import networkx as nx
import time

# === Define the Graph as an adjacency list ===
graph = {
    'A': ['B', 'C', 'F'],
    'B': ['D', 'E'],
    'C': ['F', 'E'],
    'D': ['C', 'A'],
    'E': ['G', 'A'],
    'F': ['D', 'E', 'B', 'G'],
    'G': ['D', 'B', 'C']
}

# === DFS Visualization ===
def dfs_visualize(graph, start, goal):
    visited = set()
    stack = [[start]]
    explored_edges = []
    visited_nodes = []

    G = nx.DiGraph()
    for node in graph:
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G, seed=42)

    while stack:
        path = stack.pop()
        node = path[-1]

        if node not in visited:
            visited.add(node)
            visited_nodes.append(node)

            # === Visualization Step ===
            fig, ax = plt.subplots(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color='skyblue',
                    edge_color='gray', node_size=1800, font_size=14, ax=ax)

            nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color='lightgreen', node_size=2000, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=explored_edges, edge_color='orange', width=2, ax=ax)

            ax.set_title(f"DFS Visiting: {node}", fontsize=18)
            plt.tight_layout()
            plt.show()  # Show step-by-step (close to continue)

            if node == goal:
                path_edges = list(zip(path, path[1:]))
                fig, ax = plt.subplots(figsize=(8, 6))
                nx.draw(G, pos, with_labels=True, node_color='skyblue',
                        edge_color='gray', node_size=1800, font_size=14, ax=ax)
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lime', node_size=2200, ax=ax)
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
                ax.set_title(f"✅ Goal Reached: {' -> '.join(path)}", fontsize=16)
                plt.tight_layout()
                plt.show()
                return path

            for neighbor in reversed(graph[node]):  # reverse for correct DFS order
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)
                    explored_edges.append((node, neighbor))

    print("❌ Goal Not Found")
    return None

# === Run DFS Visualization ===
start_node = 'A'
goal_node = 'G'
final_path = dfs_visualize(graph, start_node, goal_node)

if final_path:
    print("✅ Final Path:", " -> ".join(final_path))
else:
    print("❌ No Path Found")
