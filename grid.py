# Cell types
EMPTY = 0
OBSTACLE = 1
START = 2
GOAL = 3
def create_grid(rows, cols):
    """
    Create an empty grid.
    """
    return [
        [EMPTY for _ in range(cols)]
        for _ in range(rows)
    ]
def set_start(grid, current_start, row, col):
    """
    Set the agent's starting position.
    """
    if current_start is not None:
        old_row, old_col = current_start
        grid[old_row][old_col] = EMPTY
    if grid[row][col] != OBSTACLE:
        grid[row][col] = START
        return (row, col)
    return current_start
def set_goal(grid, current_goal, row, col):
    """
    Set the agent's goal position.
    """
    # Remove previous goal
    if current_goal is not None:
        old_row, old_col = current_goal
        grid[old_row][old_col] = EMPTY
    # Do not place goal on an obstacle
    if grid[row][col] != OBSTACLE:
        grid[row][col] = GOAL
        return (row, col)
    return current_goal
def add_obstacle(grid, row, col):
    """
    Add an obstacle to a cell.
    """
    # Don't overwrite start or goal
    if (
        grid[row][col] != START
        and grid[row][col] != GOAL
    ):
        grid[row][col] = OBSTACLE
def erase_cell(grid, row, col):
    """
    Make a cell empty.
    """
    grid[row][col] = EMPTY