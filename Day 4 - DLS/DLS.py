import matplotlib.pyplot as plt
import networkx as nx

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

# === DLS Visualization ===
def dls_visualize(graph, start, goal, depth_limit):
    visited = set()
    explored_edges = []
    visited_nodes = []

    # Build the graph for visualization
    G = nx.DiGraph()
    for node in graph:
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)
    pos = nx.spring_layout(G, seed=42)

    # === Recursive DLS Helper ===
    def recursive_dls(path, depth):
        node = path[-1]
        visited.add(node)
        visited_nodes.append(node)

        # === Visualization ===
        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='skyblue',
                edge_color='gray', node_size=1800, font_size=14, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color='lightgreen', node_size=2000, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=explored_edges, edge_color='orange', width=2, ax=ax)
        ax.set_title(f"Visiting: {node} | Depth: {depth}", fontsize=18)
        plt.tight_layout()
        plt.show()

        if node == goal:
            path_edges = list(zip(path, path[1:]))
            fig, ax = plt.subplots(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, node_color='skyblue',
                    edge_color='gray', node_size=1800, font_size=14, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lime', node_size=2200, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
            ax.set_title(f"✅ Goal Found: {' -> '.join(path)}", fontsize=16)
            plt.tight_layout()
            plt.show()
            return path

        if depth == 0:
            return None

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                explored_edges.append((node, neighbor))
                result = recursive_dls(path + [neighbor], depth - 1)
                if result:
                    return result
        return None

    return recursive_dls([start], depth_limit)

# === Run DLS Visualization ===
start_node = 'A'
goal_node = 'G'
depth_limit = 3  # Change this value as needed

final_path = dls_visualize(graph, start_node, goal_node, depth_limit)

if final_path:
    print("✅ Final Path:", " -> ".join(final_path))
else:
    print("❌ No Path Found within depth limit:", depth_limit)
