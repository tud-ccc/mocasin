# Copyright (C) 2018 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

import sys
import tkinter as tk

from mocasin.maps.platform import MapsPlatform
from mocasin.maps.graph import MapsDataflowGraph
from mocasin.mapper.random import RandomMapper


from mocasin.gui.testPlatform import TestPlatform
from mocasin.gui.drawAPI import drawAPI

sys.path.append("../..")


class controlPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        gettrace = getattr(sys, "gettrace", None)
        self.__path = None
        if gettrace is None:
            self.__path = sys.path[1] + "/apps/audio_filter.cpn.xml"
        elif gettrace():
            """In case of an attached debugger the sys.path list will change"""
            self.__path = sys.path[2] + "/apps"
        else:
            self.__path = sys.path[1] + "/apps"
        self.__graphInstance = MapsDataflowGraph(
            "MapsDataflowGraph", "apps/audio_filter/audio_filter.cpn.xml"
        )
        self.__platform = None
        self.__mappingIDs = []

        self.loadExButton = tk.Button(
            text="Load Exynos", command=self.__loadExynos
        )
        self.loadExButton.grid(sticky="EW", row=0)
        self.loadPaButton = tk.Button(
            text="Load Parallella", command=self.__loadParallella
        )
        self.loadPaButton.grid(sticky="EW", row=1)
        self.loadMdButton = tk.Button(
            text="Load MultiDSP", command=self.__loadMultiDSP
        )
        self.loadMdButton.grid(sticky="EW", row=2)
        self.addMappingButton = tk.Button(
            text="Add random mapping",
            state="disabled",
            command=self.__addRandomMapping,
        )
        self.addMappingButton.grid(sticky="EW", row=3)
        self.idTextBox = tk.Text(height=1, width=20, state="disabled")
        self.idTextBox.grid(sticky="EW", row=4)
        self.removeLastMappingButton = tk.Button(
            text="Remove last mapping",
            state="disabled",
            command=self.__removeLastMapping,
        )
        self.removeLastMappingButton.grid(sticky="EW", row=5)
        self.toggleNamesButton = tk.Button(
            text="Toggle task names",
            command=self.parent.drawPanel.drawDevice.toggleTaskNames,
        )
        self.toggleNamesButton.grid(sticky="EW", row=6)
        self.toggleDaDButton = tk.Button(
            text="Toggle DaD function",
            command=self.parent.drawPanel.drawDevice.toggleDragAndDrop,
        )
        self.toggleDaDButton.grid(sticky="EW", row=7)
        self.exitButton = tk.Button(text="Exit", command=root.destroy)
        self.exitButton.grid(sticky="EW", row=8)

    def __loadExynos(self):
        # platform =  MapsPlatform('MapsPlatform', 'apps/audio_filter/exynos/exynos.platform')
        platform = TestPlatform()
        self.__platform = platform
        self.parent.drawPanel.drawDevice.setPlatform(platform)
        self.loadPaButton["state"] = "disabled"
        self.loadMdButton["state"] = "disabled"
        self.addMappingButton["state"] = "normal"

    def __loadParallella(self):
        platform = MapsPlatform(
            "MapsPlatform", "apps/audio_filter/parallella/parallella.platform"
        )
        self.__platform = platform
        self.parent.drawPanel.drawDevice.setPlatform(platform)
        self.loadExButton["state"] = "disabled"
        self.loadMdButton["state"] = "disabled"
        self.addMappingButton["state"] = "normal"

    def __loadMultiDSP(self):
        platform = MapsPlatform(
            "MapsPlatform", "apps/audio_filter/multidsp/multidsp.platform"
        )
        self.__platform = platform
        self.parent.drawPanel.drawDevice.setPlatform(platform)
        self.loadExButton["state"] = "disabled"
        self.loadPaButton["state"] = "disabled"
        self.addMappingButton["state"] = "normal"

    def __addRandomMapping(self):
        mapper = RandomMapper(self.__graphInstance, self.__platform)
        mapping = mapper.generate_mapping()
        mappingID = self.parent.drawPanel.drawDevice.addMapping(mapping)
        self.__mappingIDs.append(mappingID)
        self.removeLastMappingButton["state"] = "normal"
        if len(self.__mappingIDs) > 9:
            self.addMappingButton["state"] = "disabled"
        self.__propertyChanged()

    def __removeLastMapping(self):
        mappingID = self.__mappingIDs.pop()
        self.parent.drawPanel.drawDevice.removeMapping(mappingID)
        self.addMappingButton["state"] = "normal"
        if len(self.__mappingIDs) == 0:
            self.removeLastMappingButton["state"] = "disabled"
        self.__propertyChanged()

    def __propertyChanged(self):
        self.idTextBox["state"] = "normal"
        self.idTextBox.delete(1.0, tk.END)
        for mID in self.__mappingIDs:
            if self.__mappingIDs.index(mID) == 0:
                self.idTextBox.insert(tk.END, str(mID))
            else:
                self.idTextBox.insert(tk.END, ", " + str(mID))
        self.idTextBox["state"] = "disabled"


class drawPanel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.__canvas = tk.Canvas(width=1000, height=750)
        self.__canvas.grid(row=0, column=1, rowspan=9)
        self.drawDevice = drawAPI(self.__canvas, 5, 15, 1000, 750)


class mainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.drawPanel = drawPanel(self)
        self.controlPanel = controlPanel(self)


if __name__ == "__main__":
    root = tk.Tk()
    mainWindow(root)
    root.mainloop()
