import heapq
from grid import OBSTACLE
def heuristic(current, goal):
    """
    Calculate the Manhattan distance between
    the current cell and the goal cell.
    """
    current_row, current_col = current
    goal_row, goal_col = goal
    return (
        abs(current_row - goal_row)
        + abs(current_col - goal_col)
    )
def get_neighbors(grid, current):
    """
    Find all valid neighboring cells.

    The agent can move:
    UP, DOWN, LEFT, RIGHT
    """
    rows = len(grid)
    cols = len(grid[0])
    row, col = current
    possible_moves = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]
    neighbors = []
    for row_change, col_change in possible_moves:
        new_row = row + row_change
        new_col = col + col_change
        #check for grid boundaries
        if new_row < 0 or new_row >= rows:
            continue
        if new_col < 0 or new_col >= cols:
            continue
        # do not move from obstacles
        if grid[new_row][new_col] == OBSTACLE:
            continue
        neighbors.append((new_row, new_col))
    return neighbors
def reconstruct_path(came_from, start, goal):
    """
    Reconstruct the final path after the goal
    has been reached.
    """
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    #reverse the path from start -> goal
    path.reverse()
    return path
def calculate_path_cost(path):
    """
    Calculate the total cost of the path.

    Each movement currently has a cost of 1.
    """
    if path is None:
        return 0
    return len(path) - 1
def get_path_analysis(path, goal):
    """
    Calculate A* values for every cell
    in the final path.

    g(n) = actual cost from Start to n
    h(n) = Manhattan distance from n to Goal
    f(n) = g(n) + h(n)

    Returns a list of dictionaries that
    can be displayed by the GUI.
    """
    analysis = []
    if path is None:
        return analysis
    for index, current in enumerate(path):
        g_score = index
        h_score = heuristic(
            current,
            goal
        )
        f_score = (
            g_score
            + h_score
        )
        analysis.append(
            {
                "Cell": str(current),
                "g(n) - Cost": g_score,
                "h(n) - Heuristic": h_score,
                "f(n) - Total": f_score
            }
        )
    return analysis
def astar(grid, start, goal):
    """
    Perform A* search.

    Returns:
        path       -> final path from start to goal
        explored   -> cells explored by A*
    """
    #Priority Queue
    open_set = []
    heapq.heappush(
        open_set,
        (0, start)
    )
    came_from = {}
    g_score = {
        start: 0
    }
    explored = set()
    while open_set:
        # Get the cell woth lowest priority
        current_f, current = heapq.heappop(
            open_set
        )
        if current in explored:
            continue
        # Mark current cell as explored
        explored.add(current)
        # Goal check
        if current == goal:

            path = reconstruct_path(
                came_from,
                start,
                goal
            )
            return path, explored
            # Get neighbours
        neighbors = get_neighbors(
            grid,
            current
        )
        for neighbor in neighbors:
            # Every movement costs 1
            movement_cost = 1
            # Calculate cost from start
            tentative_g = (
                g_score[current]
                + movement_cost
            )
            # check fro best path
            if (
                neighbor not in g_score
                or tentative_g < g_score[neighbor]
            ):
                # Remember the parent
                came_from[neighbor] = current

                # Store the cost
                g_score[neighbor] = tentative_g

                #calcuate the heuristic
                h_score = heuristic(
                    neighbor,
                    goal
                )
                f_score = (
                    tentative_g
                    + h_score
                )
                # Add neighbor to priority queue
                heapq.heappush(
                    open_set,
                    (f_score, neighbor)
                )
    return None, explored