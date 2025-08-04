import matplotlib.pyplot as plt
import networkx as nx
import heapq

# === Define the Graph with weighted edges ===
graph = {
    'A': [('B', 1), ('C', 4), ('F', 3)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 1), ('E', 2)],
    'D': [('C', 3), ('A', 6)],
    'E': [('G', 2), ('A', 4)],
    'F': [('D', 2), ('E', 1), ('B', 3), ('G', 5)],
    'G': [('D', 1), ('B', 2), ('C', 4)]
}

# === UCS Visualization ===
def ucs_visualize(graph, start, goal):
    visited = set()
    queue = [(0, [start])]  # (cost, path)
    explored_edges = []
    visited_nodes = []

    # Build graph for visualization
    G = nx.DiGraph()
    for node in graph:
        for neighbor, cost in graph[node]:
            G.add_edge(node, neighbor, weight=cost)
    pos = nx.spring_layout(G, seed=42)

    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]

        if node not in visited:
            visited.add(node)
            visited_nodes.append(node)

            # === Visualization ===
            fig, ax = plt.subplots(figsize=(8, 6))
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw(G, pos, with_labels=True, node_color='skyblue',
                    edge_color='gray', node_size=1800, font_size=14, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

            nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color='lightgreen', node_size=2000, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=explored_edges, edge_color='orange', width=2, ax=ax)

            ax.set_title(f"UCS Visiting: {node} | Cost: {cost}", fontsize=18)
            plt.tight_layout()
            plt.show()

            if node == goal:
                path_edges = list(zip(path, path[1:]))
                fig, ax = plt.subplots(figsize=(8, 6))
                nx.draw(G, pos, with_labels=True, node_color='skyblue',
                        edge_color='gray', node_size=1800, font_size=14, ax=ax)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lime', node_size=2200, ax=ax)
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
                ax.set_title(f"✅ Goal Found: {' -> '.join(path)} | Total Cost: {cost}", fontsize=16)
                plt.tight_layout()
                plt.show()
                return path, cost

            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    heapq.heappush(queue, (cost + weight, new_path))
                    explored_edges.append((node, neighbor))

    print("❌ Goal Not Found")
    return None, None

# === Run UCS Visualization ===
start_node = 'A'
goal_node = 'G'
final_path, total_cost = ucs_visualize(graph, start_node, goal_node)

if final_path:
    print("✅ Final Path:", " -> ".join(final_path))
    print("🧾 Total Cost:", total_cost)
else:
    print("❌ No Path Found")
