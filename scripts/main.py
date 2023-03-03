from pathlib import Path
from functools import partial

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


def gallery_refresh(directory: Path):
    return sorted(map(str, directory.glob("*.png")), reverse=True)


def gallery_event(elem_id):
    # TODO: impl download
    pass


def outputs_tab():
    output_directory = Path(scripts.basedir()) / "outputs"

    with gr.Blocks(analytics_enabled=False) as outputs_tab:
        if not output_directory.exists():
            gr.Button(value="Output Empty", label="Output Empty", disabled=True)

        else:
            for task_directory in sorted(output_directory.iterdir(), reverse=True):
                if not task_directory.is_dir():
                    continue

                with gr.Accordion(task_directory.name, open=True):
                    for date_directory in sorted(
                        task_directory.iterdir(), reverse=True
                    ):
                        if not date_directory.is_dir():
                            continue

                        with gr.Accordion(date_directory.name, open=False):
                            refresh_btn = gr.Button(
                                value="Refresh", label="Refresh", disabled=True
                            )

                            gallery = gr.Gallery(
                                label="Generated images",
                                show_label=False,
                                value=sorted(
                                    map(str, date_directory.glob("*.png")), reverse=True
                                ),
                                elem_id=f"{task_directory}_{date_directory}",
                            ).style(grid=[8], height="auto")

                            refresh_btn.click(
                                partial(
                                    gallery_refresh,
                                    directory=date_directory,
                                ),
                                inputs=[],
                                outputs=[gallery],
                            )

        return [(outputs_tab, "Outputs", "outputs_tab")]


script_callbacks.on_ui_tabs(outputs_tab)
