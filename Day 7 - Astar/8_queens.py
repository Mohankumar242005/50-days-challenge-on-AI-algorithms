import heapq

N = 8

# --- Heuristic: Number of attacking pairs ---
def heuristic(state):
    attacks = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

# --- Generate neighbors by placing queen in next column ---
def get_neighbors(state):
    neighbors = []
    col = len(state)
    if col >= N:
        return neighbors
    for row in range(N):
        new_state = state + [row]
        neighbors.append(new_state)
    return neighbors

# --- A* for N-Queens ---
def a_star_n_queens():
    open_list = []
    heapq.heappush(open_list, (heuristic([]), 0, []))  # (f = h + g, g = depth, state)

    while open_list:
        f, g, state = heapq.heappop(open_list)

        if len(state) == N and heuristic(state) == 0:
            print("✅ Solution:", state)
            print_board(state)
            return state

        for neighbor in get_neighbors(state):
            h = heuristic(neighbor)
            heapq.heappush(open_list, (g + 1 + h, g + 1, neighbor))
    return None

# --- Print board ---
def print_board(state):
    for row in range(N):
        line = ""
        for col in range(N):
            line += "Q " if col == state[row] else ". "
        print(line)
    print()

# --- Run it ---
a_star_n_queens()
