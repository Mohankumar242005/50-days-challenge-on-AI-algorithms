import networkx as nx
import matplotlib.pyplot as plt
import heapq
import time

# -------------------------
# Beam Search Implementation
# -------------------------
def beam_search(graph, start, goal, beam_width, heuristic):
    # Priority queue with (heuristic, path)
    queue = [(heuristic[start], [start])]
    
    visited_paths = []
    
    while queue:
        # Sort by heuristic (best first)
        queue.sort(key=lambda x: x[0])
        
        # Keep only the best 'beam_width' candidates
        queue = queue[:beam_width]
        
        next_queue = []
        
        for cost, path in queue:
            current_node = path[-1]
            visited_paths.append(list(path))
            
            if current_node == goal:
                return path, visited_paths
            
            for neighbor in graph.neighbors(current_node):
                if neighbor not in path:
                    new_path = path + [neighbor]
                    heapq.heappush(next_queue, (heuristic[neighbor], new_path))
        
        queue = next_queue
    
    return None, visited_paths


# -------------------------
# Visualization
# -------------------------
def visualize_graph(graph, visited_paths, goal):
    pos = nx.spring_layout(graph)
    
    for path in visited_paths:
        plt.clf()
        nx.draw(graph, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=10)
        edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges_in_path, width=2, edge_color="red")
        
        if goal in path:
            nx.draw_networkx_nodes(graph, pos, nodelist=[goal], node_color="green", node_size=800)
        
        plt.pause(1)
    plt.show()


# -------------------------
# Example Graph + Run
# -------------------------
if __name__ == "__main__":
    # Create graph
    G = nx.Graph()
    edges = [
        ('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'),
        ('C', 'F'), ('C', 'G'), ('E', 'H'), ('F', 'I'),
        ('G', 'J')
    ]
    G.add_edges_from(edges)
    
    # Heuristic values (simulating straight-line distances)
    heuristic = {
        'A': 7, 'B': 6, 'C': 4, 'D': 4, 'E': 2,
        'F': 5, 'G': 1, 'H': 1, 'I': 3, 'J': 0
    }
    
    start_node = 'A'
    goal_node = 'J'
    beam_width = 2
    
    path, visited_paths = beam_search(G, start_node, goal_node, beam_width, heuristic)
    
    print("Final Path Found:", path)
    
    visualize_graph(G, visited_paths, goal_node)
