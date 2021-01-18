# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

import hydra
import tkinter as tk

from mocasin.gui.drawAPI import drawAPI


@hydra.main(config_path="../conf", config_name="visualize")
def visualize(cfg):
    graph = hydra.utils.instantiate(cfg["graph"])
    platform = hydra.utils.instantiate(cfg["platform"])
    trace = hydra.utils.instantiate(cfg["trace"])
    representation = hydra.utils.instantiate(
        cfg["representation"], graph, platform
    )
    mapping = hydra.utils.instantiate(
        cfg["mapper"], graph, platform, trace, representation
    ).generate_mapping()
    task_names = cfg["task_names"]
    width = cfg["width"]
    height = cfg["height"]

    root = tk.Tk()
    window(root, platform, mapping, task_names, width, height)
    root.mainloop()


class window(tk.Frame):
    def __init__(self, parent, platform, mapping, task_names, width, height):
        self.parent = parent
        m_canvas = tk.Canvas(width=width, height=height)
        m_canvas.grid()

        self.api_instance = drawAPI(m_canvas, 5, 15, width, height)

        if not task_names:
            self.api_instance.toggleTaskNames()
        self.api_instance.setPlatform(platform)
        self.api_instance.addMapping(mapping)
