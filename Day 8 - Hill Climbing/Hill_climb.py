import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D

# === 1. Define a 2D hill function (surface) ===
def hill_function(x, y):
    return -1 * ((x - 3)**2 + (y - 2)**2) + 10  # Peak at (3, 2), max value = 10

# === 2. 2D Hill Climbing algorithm ===
def hill_climbing_2d(start_x, start_y, step_size=0.1, max_iter=100):
    path = [(start_x, start_y, hill_function(start_x, start_y))]
    current_x, current_y = start_x, start_y

    for i in range(max_iter):
        current_z = hill_function(current_x, current_y)

        # Generate 8 neighbors around the current position
        neighbors = [
            (current_x + step_size, current_y),
            (current_x - step_size, current_y),
            (current_x, current_y + step_size),
            (current_x, current_y - step_size),
            (current_x + step_size, current_y + step_size),
            (current_x - step_size, current_y - step_size),
            (current_x + step_size, current_y - step_size),
            (current_x - step_size, current_y + step_size),
        ]

        # Evaluate all neighbors
        best_neighbor = max(neighbors, key=lambda p: hill_function(p[0], p[1]))
        best_z = hill_function(best_neighbor[0], best_neighbor[1])

        if best_z <= current_z:
            break  # No better neighbor → stop

        current_x, current_y = best_neighbor
        path.append((current_x, current_y, best_z))

    return path

# === 3. Visualization ===
def visualize_2d_hill(path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create surface data
    x = np.linspace(0, 6, 100)
    y = np.linspace(0, 6, 100)
    X, Y = np.meshgrid(x, y)
    Z = hill_function(X, Y)

    # Plot surface
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)

    # Plot path
    px = [p[0] for p in path]
    py = [p[1] for p in path]
    pz = [p[2] for p in path]
    ax.plot(px, py, pz, 'ro-', label='Climbing Path')

    # Final point (peak)
    ax.scatter(px[-1], py[-1], pz[-1], color='green', s=100, label='Peak')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Elevation (Z)')
    ax.set_title('2D Hill Climbing')
    ax.legend()
    plt.show()

# === 4. Main Execution ===
if __name__ == "__main__":
    start_x = random.uniform(0, 6)
    start_y = random.uniform(0, 6)
    print(f"⛰️ Starting Hill Climb from x={start_x:.2f}, y={start_y:.2f}")

    path = hill_climbing_2d(start_x, start_y)
    
    print("🧗 Path Taken:")
    for i, (x, y, z) in enumerate(path):
        print(f"  Step {i}: x = {x:.2f}, y = {y:.2f}, z = {z:.2f}")

    print(f"🏁 Reached Peak at x={path[-1][0]:.2f}, y={path[-1][1]:.2f}, z={path[-1][2]:.2f}")
    
    visualize_2d_hill(path)
