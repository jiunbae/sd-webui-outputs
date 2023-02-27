from pathlib import Path

import gradio as gr

import modules.scripts as scripts
from modules import script_callbacks


class Script(scripts.Script):
    def title(self):
        return "Outputs"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        return ()


def gallery_event(elem_id):
    # TODO: impl download
    pass


def outputs_tab():
    output_directory = Path(scripts.basedir()) / "outputs"

    with gr.Blocks(analytics_enabled=False) as outputs_tab:
        if not output_directory.exists():
            gr.Button(value="Output Empty", label="Output Empty", disabled=True)

        else:
            for task_directory in output_directory.iterdir():
                if not task_directory.is_dir():
                    continue

                with gr.Accordion(task_directory.name, open=True):
                    for date_directory in task_directory.iterdir():
                        if not date_directory.is_dir():
                            continue

                        with gr.Accordion(date_directory.name, open=False):

                            gallery = gr.Gallery(
                                label="Generated images",
                                show_label=False,
                                value=sorted(map(str, date_directory.glob("*.png"))),
                                elem_id=f"{task_directory}_{date_directory}",
                            ).style(grid=[8], height="auto")

        return [(outputs_tab, "Outputs", "outputs_tab")]


script_callbacks.on_ui_tabs(outputs_tab)
