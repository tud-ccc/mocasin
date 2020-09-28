# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import hydra
import tkinter as tk

from pykpn.gui.drawAPI import drawAPI


@hydra.main(config_path='../conf', config_name='visualize')
def visualize(cfg):
    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])
    mapping = hydra.utils.instantiate(cfg['mapper'], kpn, platform, cfg).generate_mapping()
    task_names = cfg['task_names']
    width = cfg['width']
    height = cfg['height']

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
