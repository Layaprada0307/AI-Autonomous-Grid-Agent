from grid import create_grid, OBSTACLE
from astar import astar
# Create a 5 x 5 grid
grid = create_grid(5, 5)
# Add some obstacles
grid[1][1] = OBSTACLE
grid[1][2] = OBSTACLE
grid[2][2] = OBSTACLE
grid[3][2] = OBSTACLE
# Define start and goal
start = (0, 0)
goal = (4, 4)
# Run A*
path, explored = astar(
    grid,
    start,
    goal
)
# Display results
print("Start:", start)
print("Goal:", goal)
print("\nPath:")
if path is not None:
    for position in path:
        print(position)
else:
    print("No path found.")
print("\nNumber of explored cells:", len(explored))