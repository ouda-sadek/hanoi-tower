import streamlit as st
from solve import HanoiSolver

st.set_page_config(page_title="Hanoi Tower", layout="centered")
st.title("Tower of Hanoi Game")

# ---- 1. User input: number of discs and rods----
disk_count = st.slider("Number of disks", min_value=1, max_value=10, value=3)
peg_count = st.slider("Number of stems", min_value=3, max_value=5, value=3)

# ---- 2. Storage in session_state ----
if "solver" not in st.session_state or st.session_state.disk_count != disk_count or st.session_state.peg_count != peg_count:
    solver = HanoiSolver(disk_count, peg_count)
    moves = solver.solve()
    st.session_state.solver = solver
    st.session_state.moves = moves
    st.session_state.current_step = 0
    st.session_state.disk_count = disk_count
    st.session_state.peg_count = peg_count

# ---- 3. Button: automatic resolution----
if st.button("Solve automatically"):
    for i, move in enumerate(st.session_state.moves):
        st.write(f"{i+1}. Move a disk from {move[0]} → {move[1]}")
    st.success(f"Solved in {len(st.session_state.moves)} moves.")

# ---- 4. Step by step resolution----
if st.button("Next step"):
    if st.session_state.current_step < len(st.session_state.moves):
        move = st.session_state.moves[st.session_state.current_step]
        st.write(f"Stage {st.session_state.current_step+1} : {move[0]} → {move[1]}")
        st.session_state.current_step += 1
    else:
        st.info("All the trips have been made.")

# ---- 5. Reset ----
if st.button("Reset"):
    st.session_state.clear()
    st.experimental_rerun()

# ---- 6. Simplified graphical display----

def display_state(moves, disk_count, peg_count, step):
    # Initialize stems: stack list
    pegs = [[] for _ in range(peg_count)]
    for i in reversed(range(disk_count)):
        pegs[0].append(i)  # All discs at the start

    # Apply moves to the given step
    for move in moves[:step]:
        from_peg, to_peg = move[0] - 1, move[1] - 1
        disk = pegs[from_peg].pop()
        pegs[to_peg].append(disk)

    # Visual rendering with rich text
    st.subheader("Visualization of the position of the disks")
    for level in range(disk_count - 1, -1, -1):
        row = ""
        for peg in pegs:
            if level < len(peg):
                disk_size = peg[level]
                color = DISK_COLORS[disk_size % len(DISK_COLORS)]
                width = 8 + disk_size * 4
                row += f'<div style="display:inline-block;width:{width}px;background:{color};margin:5px;height:20px;border-radius:5px;"></div>'
            else:
                row += f'<div style="display:inline-block;width:40px;margin:5px;height:20px;"></div>'
        st.markdown(row, unsafe_allow_html=True)

DISK_COLORS = ["#E57373", "#FFB74D", "#FFF176", "#81C784", "#64B5F6", "#BA68C8"]

# Call the function to display the current state
display_state(
    st.session_state.moves,
    st.session_state.disk_count,
    st.session_state.peg_count,
    st.session_state.current_step
)
