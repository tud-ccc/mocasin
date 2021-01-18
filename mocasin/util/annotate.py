# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Gerald Hempel

import math
import matplotlib.pyplot as plt


class AnnoteFinder(object):
    """callback for matplotlib to display an annotation when points are
    clicked on.  The point which is closest to the click and within
    xtol and ytol is identified.

    Register this function like this:

    scatter(xdata, ydata)
    af = AnnoteFinder(xdata, ydata, annotes)
    connect('button_press_event', af)
    """

    def __init__(self, xdata, ydata, annotes, ax=None, xtol=None, ytol=None):
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None:
            xtol = ((max(xdata) - min(xdata)) / float(len(xdata))) / 2
        if ytol is None:
            ytol = ((max(ydata) - min(ydata)) / float(len(ydata))) / 2

        # Lower bound of sensitivity area is 10 pixel.
        # This may cause imprecise behaviour for dense scatter plots!
        if 10 > xtol:
            xtol = 10
        if 10 > ytol:
            ytol = 10

        self.xtol = xtol
        self.ytol = ytol

        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        self.drawnAnnotations = []
        self.links = []

    def distance(self, x1, x2, y1, y2):
        """
        return the (euclidian) distance between two points
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __call__(self, event):

        if event.inaxes:

            clickX = event.xdata
            clickY = event.ydata
            if (self.ax is None) or (self.ax is event.inaxes):
                annotes = []
                # print(event.xdata, event.ydata)
                for x, y, a in self.data:
                    # print(x, y, a)
                    if (clickX - self.xtol < x < clickX + self.xtol) and (
                        clickY - self.ytol < y < clickY + self.ytol
                    ):
                        annotes.append(
                            (self.distance(x, clickX, y, clickY), x, y, a)
                        )
                if annotes:
                    annotes.sort()
                    distance, x, y, annote = annotes[0]
                    self.drawAnnote(event.inaxes, x, y, annote)
                    for l in self.links:
                        l.drawSpecificAnnote(annote)

    def drawAnnote(self, ax, x, y, annote):
        """
        Draw the annotation on the plot
        (uses mathplotlib annotate function with some fancy design)
        """
        # from matplotlib.lines import Line2D
        if self.drawnAnnotations:
            for a in self.drawnAnnotations:
                a.set_visible(not a.get_visible())
            self.drawnAnnotations = []
            self.ax.figure.canvas.draw_idle()
        else:
            lenX = ax.get_xlim()[1] - ax.get_xlim()[0]
            lenY = ax.get_ylim()[1] - ax.get_xlim()[0]
            boxPosX = ax.get_xlim()[1] + 0.1 * lenX
            boxPosY = ax.get_ylim()[1] - 0.5 * lenY

            ann = ax.annotate(
                " %s" % (annote),
                xy=(x, y),
                xycoords="data",
                xytext=(boxPosX, boxPosY),
                textcoords="data",
                size=10,
                va="center",
                ha="left",
                family="monospace",
                bbox=dict(boxstyle="round", pad=0.6, alpha=0.2, fc="w"),
                arrowprops=dict(
                    arrowstyle="-|>, head_length=0.8,head_width=0.4",
                    connectionstyle="arc3,rad=-0.2",
                    fc="w",
                ),
            )

            self.drawnAnnotations.append(ann)
            self.ax.figure.canvas.draw_idle()

    def drawSpecificAnnote(self, annote):
        annotesToDraw = [(x, y, a) for x, y, a in self.data if a == annote]
        for x, y, a in annotesToDraw:
            self.drawAnnote(self.ax, x, y, a)
