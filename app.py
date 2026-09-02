import gradio as gr
from src.maze_solver import MazeSolver



def submit_img(input_img):
	global solver

	#Initializing the maze solver
	solver=MazeSolver(input_img)

	return (
		True,
		gr.update(value=solver.bin_img, interactive=False, label="Select start & end"),
		gr.update(visible=False),
		gr.update(visible=False),
		gr.update(visible=False)
	)

def samples_btn_click(sample_num):
	return f"examples/sample_{sample_num}.png"


def inp_img_click(image, is_img_clickable, evt: gr.SelectData):
	global solver

	if not is_img_clickable:
		return is_img_clickable, image, "Solve!"

	#Setting the start and end point of maze
	new_image=solver.set_start_end_pt(image, evt.index)

	solve_btn_vis=False
	if solver.start_pt!=None and solver.end_pt!=None:
		is_img_clickable=False
		solve_btn_vis=True

	return is_img_clickable, new_image, gr.update(visible=solve_btn_vis)



def solve_btn_click():
	#Calling solve function
	output_img=solver.solve()

	return output_img, gr.update(visible=True), gr.update(visible=True)



def restart():
	return (
		gr.update(interactive=True, label="Maze", value=None),
		False,
		gr.update(visible=True),
		gr.update(visible=True),
		gr.update(visible=True),
		gr.update(visible=False),
		gr.update(visible=False),
		gr.update(visible=False)
	)




with gr.Blocks(title="Maze Solver") as demo:
	with gr.Row():
		with gr.Column():
			input_image=gr.Image(width="100%", label="Maze")
			is_img_clickable=gr.State(False)

			with gr.Row():
				sample_number=gr.Dropdown(
					choices=[
						("Sample 1", 1),
						("Sample 2", 2),
						("Sample 3", 3),
					],
					show_label=False,
					container=False
				)
				samples_btn=gr.Button("Try Sample")

			submit_btn=gr.Button("Submit", variant="primary", visible=True)
			solve_btn=gr.Button("Slove!", variant="primary", visible=False)

		with gr.Column():
			output_image=gr.Image(width="100%", label="output", visible=False)
			restart_btn=gr.Button("Restart", visible=False)
	


	samples_btn.click(
		fn=samples_btn_click,
		inputs=sample_number,
		outputs=input_image,
	)

	submit_btn.click(
		fn=submit_img,
		inputs=input_image,
		outputs=[
			is_img_clickable,
			input_image,
			submit_btn,
			samples_btn,
			sample_number
		],
	)
	input_image.select(
		fn=inp_img_click,
		inputs=[input_image, is_img_clickable],
		outputs=[is_img_clickable, input_image, solve_btn]
	)
	solve_btn.click(
		fn=solve_btn_click,
		outputs=[output_image, output_image, restart_btn],
	)
	restart_btn.click(
		fn=restart,
		outputs=[
			input_image,
			is_img_clickable,
			samples_btn,
			sample_number,
			submit_btn,
			solve_btn,
			output_image,
			restart_btn
		],
	)


demo.launch()