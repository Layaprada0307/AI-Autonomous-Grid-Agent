import streamlit as st
from grid import (
    OBSTACLE,
    START,
    GOAL,
    create_grid,
    set_start,
    set_goal,
    add_obstacle,
    erase_cell
)
from astar import (
    astar,
    calculate_path_cost,
    get_path_analysis
)
st.set_page_config(
    page_title="Autonomous Grid Agent",
    page_icon="🤖"
)
st.title("🤖 Autonomous Grid Agent")
st.write(
    "Create an environment for the AI agent by "
    "setting a start point, goal, and obstacles."
)
ROWS = 10
COLS = 10
if "grid" not in st.session_state:
    st.session_state.grid = create_grid(
        ROWS,
        COLS
    )
if "start" not in st.session_state:
    st.session_state.start = None
if "goal" not in st.session_state:
    st.session_state.goal = None
if "path" not in st.session_state:
    st.session_state.path = None
if "explored" not in st.session_state:
    st.session_state.explored = set()
if "search_completed" not in st.session_state:
    st.session_state.search_completed = False
#sidebar controls
st.sidebar.header("Grid Controls")
mode = st.sidebar.radio(
    "Select Mode",
    [
        "Set Start",
        "Set Goal",
        "Add Obstacles",
        "Erase"
    ]
)
#Clear search Results
def clear_search_result():
    st.session_state.path = None
    st.session_state.explored = set()
    st.session_state.search_completed = False
# handling cell clicks
def handle_cell_click(row, col):
    clear_search_result()
    if mode == "Set Start":
        st.session_state.start = set_start(
            st.session_state.grid,
            st.session_state.start,
            row,
            col
        )
    #set goal
    elif mode == "Set Goal":
        st.session_state.goal = set_goal(
            st.session_state.grid,
            st.session_state.goal,
            row,
            col
        )
    #Add Obstacles
    elif mode == "Add Obstacles":
        add_obstacle(
            st.session_state.grid,
            row,
            col
        )
    #erase
    elif mode == "Erase":
        if st.session_state.grid[row][col] == START:
            st.session_state.start = None
        if st.session_state.grid[row][col] == GOAL:
            st.session_state.goal = None
        erase_cell(
            st.session_state.grid,
            row,
            col
        )
#Preapare Path
if st.session_state.path is not None:
    path_set = set(
        st.session_state.path
    )
else:
    path_set = set()
#Grid Display
st.subheader("Grid Environment")
for row in range(ROWS):
    columns = st.columns(COLS)
    for col in range(COLS):
        position = (row, col)
        cell_value = st.session_state.grid[row][col]
        if position == st.session_state.start:
            label = "S"
        elif position == st.session_state.goal:
            label = "G"
        elif position in path_set:
            label = "★"
        elif position in st.session_state.explored:
            label = "●"
        elif cell_value == OBSTACLE:
            label = "█"
        else:
            label = "·"
        
        #Display cell
        with columns[col]:

            if st.button(
                label,
                key=f"cell_{row}_{col}"
            ):

                handle_cell_click(
                    row,
                    col
                )

                st.rerun()
st.sidebar.divider()
if st.sidebar.button("▶ Run Agent"):
    if st.session_state.start is None:
        st.warning(
            "⚠️ Please set a Start position first."
        )
    elif st.session_state.goal is None:
        st.warning(
            "⚠️ Please set a Goal position first."
        )
    else:
        path, explored = astar(
            st.session_state.grid,
            st.session_state.start,
            st.session_state.goal
        )
        #Store Results
        st.session_state.path = path
        st.session_state.explored = explored
        st.session_state.search_completed = True
        st.rerun()
if st.session_state.search_completed:
    st.divider()
    st.subheader("📊 Search Results")
    if st.session_state.path is not None:
        path_cost = calculate_path_cost(
            st.session_state.path
        )
        nodes_explored = len(
            st.session_state.explored
        )
        st.success(
            "✅ Path found successfully!"
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Path Cost",
                path_cost
            )
        with col2:
            st.metric(
                "Nodes Explored",
                nodes_explored
            )
        # A* Analysis
        st.divider()
        st.subheader("🧠 A* Path Analysis")
        st.write(
            "A* evaluates a cell using:"
        )
        st.latex(
            r"f(n) = g(n) + h(n)"
        )
        st.write(
            "**g(n)** = actual cost from Start to the cell  \n"
            "**h(n)** = estimated cost from the cell to Goal  \n"
            "**f(n)** = estimated total cost"
        )
    #Generate analysis
        analysis = get_path_analysis(
            st.session_state.path,
            st.session_state.goal
        )
#Display Table
        st.dataframe(
            analysis,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.error(
            "❌ No path exists between "
            "the Start and Goal."
        )
if st.sidebar.button("Clear Grid"):
    st.session_state.grid = create_grid(
        ROWS,
        COLS
    )
    st.session_state.start = None
    st.session_state.goal = None
    st.session_state.path = None
    st.session_state.explored = set()
    st.session_state.search_completed = False
    st.rerun()