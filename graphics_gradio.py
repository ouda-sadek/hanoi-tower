import gradio as gr
from solve import HanoiSolver

# Global storage for game state
state = {
    "moves": [],
    "step": 0,
    "disk_count": 3,
    "peg_count": 3
}

DISK_COLORS = ["#E57373", "#FFB74D", "#FFF176", "#81C784", "#64B5F6", "#BA68C8", "#A1887F", "#F06292", "#4DB6AC"]

def render_pegs(moves, step, disk_count, peg_count):
    # Initializing the stems
    pegs = [[] for _ in range(peg_count)]
    for i in reversed(range(disk_count)):
        pegs[0].append(i)

    for move in moves[:step]:
        src, tgt = move[0]-1, move[1]-1
        if not pegs[src]:
            continue  # empty source rod
        disk = pegs[src][-1]
        if not pegs[tgt] or disk < pegs[tgt][-1]:
            pegs[src].pop()
            pegs[tgt].append(disk)
        else:
            # Error: invalid movement (large over small) → we ignore
            continue

    # Building the HTML display
    html = '<div style="display:flex;justify-content:center;gap:40px;">'
    for peg_idx, peg in enumerate(pegs):
        html += '<div style="display:flex;flex-direction:column-reverse;align-items:center;height:300px;">'
        html += '<div style="width:6px;height:220px;background:black;margin-bottom:5px;"></div>'
        for disk in peg:
            width = 30 + disk * 20
            color = DISK_COLORS[disk % len(DISK_COLORS)]
            html += f'<div style="width:{width}px;height:20px;margin:2px 0;background:{color};border-radius:5px;"></div>'
        html += f'<div style="margin-top:10px;">Tige {peg_idx+1}</div>'
        html += '</div>'
    html += '</div>'
    return html

def setup_game(disk_count, peg_count):
    solver = HanoiSolver(disk_count, peg_count)
    moves = solver.solve()
    state.update({
        "disk_count": disk_count,
        "peg_count": peg_count,
        "moves": moves,
        "step": 0
    })
    return render_pegs(moves, 0, disk_count, peg_count)

def next_step():
    if state["step"] < len(state["moves"]):
        state["step"] += 1
    return render_pegs(state["moves"], state["step"], state["disk_count"], state["peg_count"])

def solve_all():
    state["step"] = len(state["moves"])
    return render_pegs(state["moves"], state["step"], state["disk_count"], state["peg_count"])

def reset_game():
    return setup_game(state["disk_count"], state["peg_count"])

with gr.Blocks() as demo:
    gr.Markdown("# Tower of Hanoi Game / Web Interface with Gradio")
    with gr.Row():
        disk_slider = gr.Slider(1, 9, value=3, step=1, label="Number of disks")
        peg_slider = gr.Slider(3, 5, value=3, step=1, label="Number of stems")
        setup_btn = gr.Button("To start up")

    output_html = gr.HTML()

    with gr.Row():
        step_btn = gr.Button("Next step")
        solve_btn = gr.Button("Solve automatically")
        reset_btn = gr.Button("Reset")

    setup_btn.click(setup_game, inputs=[disk_slider, peg_slider], outputs=output_html)
    step_btn.click(next_step, outputs=output_html)
    solve_btn.click(solve_all, outputs=output_html)
    reset_btn.click(reset_game, outputs=output_html)

if __name__ == "__main__":
    demo.launch()
