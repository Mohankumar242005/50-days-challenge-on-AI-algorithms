import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import copy
import time

# --------------------------
# AC-3 with improved viz
# --------------------------

def constraint_ok(x, y):
    # Map-coloring style constraint: values must be different
    return x != y

def revise(csp, xi, xj):
    """Remove values from domain[xi] that have no supporting value in domain[xj]. 
       Return list of removed values (empty if none)."""
    removed = []
    for val in csp['domains'][xi][:]:                # iterate over a copy
        if not any(constraint_ok(val, y) for y in csp['domains'][xj]):
            csp['domains'][xi].remove(val)
            removed.append(val)
    return removed

def visualize_step(ax, G, pos, domains, step, arc=None, removed=None, title=''):
    ax.clear()

    # Node color: assigned (domain size 1) -> lightgreen else skyblue
    node_colors = []
    for n in G.nodes():
        node_colors.append('lightgreen' if len(domains[n]) == 1 else 'skyblue')

    # Draw nodes & edges
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, ax=ax)
    nx.draw_networkx_edges(G, pos, width=1.2, ax=ax)

    # Highlight current arc if provided (drawn thicker & orange)
    if arc is not None:
        if G.has_edge(*arc):
            nx.draw_networkx_edges(G, pos, edgelist=[arc], width=3.0, edge_color='orange', ax=ax)
        else:
            # Graph may be undirected; try reversed
            nx.draw_networkx_edges(G, pos, edgelist=[(arc[1], arc[0])], width=3.0, edge_color='orange', ax=ax)

    # Prepare readable labels: variable name on first line, domain values on second
    labels = {n: f"{n}\n{','.join(domains[n])}" for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)

    # If some values were removed this step, show them in the title
    removed_text = f" | removed from {arc[0]}: {removed}" if removed else ""
    ax.set_title(f"AC-3 Step {step}: {title}{removed_text}", fontsize=10)
    ax.set_axis_off()

    plt.pause(0.8)   # small delay so you can see each step


def ac3_with_viz(csp):
    # Build graph for visualization (undirected edges)
    G = nx.Graph()
    for var, neighs in csp['neighbors'].items():
        for n in neighs:
            G.add_edge(var, n)
    pos = nx.spring_layout(G, seed=42)   # fixed layout so positions don't jump

    # Setup figure once
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 6))

    # Initialize queue with all arcs (xi, xj) for every neighbor
    queue = deque((xi, xj) for xi in csp['neighbors'] for xj in csp['neighbors'][xi])

    step = 1
    # initial visualization
    visualize_step(ax, G, pos, csp['domains'], step - 1, arc=None, removed=None, title="Initial domains")

    while queue:
        xi, xj = queue.popleft()
        removed = revise(csp, xi, xj)
        title = f"Processing arc ({xi} -> {xj})"
        visualize_step(ax, G, pos, csp['domains'], step, arc=(xi, xj), removed=removed, title=title)

        if removed:
            # If xi domain became empty -> failure
            if not csp['domains'][xi]:
                ax.set_title(f"Failure: domain of {xi} became empty", fontsize=10)
                plt.ioff()
                plt.show()
                return False

            # enqueue all arcs (xk, xi) where xk is neighbor of xi (except xj)
            for xk in csp['neighbors'][xi]:
                if xk != xj:
                    queue.append((xk, xi))

        step += 1

    # Final state
    visualize_step(ax, G, pos, csp['domains'], step, arc=None, removed=None, title="AC-3 Completed")
    plt.ioff()
    plt.show()
    return True


# --------------------------
# Example CSP (Australia map)
# --------------------------
if __name__ == "__main__":
    domains = {
        'WA': ['red', 'green', 'blue'],
        'NT': ['red', 'green', 'blue'],
        'SA': ['red', 'green', 'blue'],
        'Q':  ['red', 'green', 'blue'],
        'NSW':['red', 'green', 'blue'],
        'V':  ['red', 'green', 'blue'],
        'T':  ['red', 'green', 'blue']
    }

    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q':  ['NT', 'SA', 'NSW'],
        'NSW':['Q', 'SA', 'V'],
        'V':  ['SA', 'NSW'],
        'T':  []
    }

    csp = {'domains': copy.deepcopy(domains), 'neighbors': neighbors}

    success = ac3_with_viz(csp)
    print("AC-3 success:", success)
    print("Domains after AC-3:")
    for v, d in csp['domains'].items():
        print(f"  {v}: {d}")
