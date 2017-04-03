from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from random import randrange, random
import pyqtgraph.opengl as gl
import numpy as np

class PlotInfo3d:
    def __init__(self, name, color, description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.visible = True
        self.color = color

    name = ""
    description = ""
    xs = np.array([])
    ys = np.array([])
    zs = np.empty([0, 0])
    plot = 0

class MultiPlot3d(QWidget):
    def add_plot(self, name, color=0, description=""):
        if color == 0:
            color = (random(), random(), random(), 1)
        if name in self.__plot_data__:
            print('Plot with this name already exists!')
            return
        self.__plot_data__[name] = PlotInfo3d(name, color, description)

    def remove_plot(self, name):
        if name in self.__plot_data__:
            del self.__plot_data__[name]

    def get_plot_names(self):
        """ get_plot_names() -> [String]"""
        return self.__plot_data__.keys()

    def get_plot_info(self, name):
        """ get_plot_info(name) -> PlotInfo"""
        self.__plot_data__[name]

    def set_plot_data(self, name, xs, ys, zs, description=""):
        if name in self.__plot_data__:
            plot_info = self.__plot_data__[name]
            if description == "":
                description = plot_info.description
            plot_info.description = description
            plot_info.xs = xs
            plot_info.ys = ys
            plot_info.zs = zs
        else:
            print('No plot with this name')

    def clear_plot_data(self, name):
        if name in self.__plot_data__:
            plot_info = self.__plot_data__[name]
            plot_info.xs = []
            plot_info.ys = []
            plot_info.zs = []
        else:
            print('No plot with this name')

    def refresh(self):
        self.__legend_model__.clear()
        for key in self.__plot_data__:
            item = QStandardItem()
            description = self.__plot_data__[key].description
            item.setText(key)
            item.setCheckable(True)
            item.setCheckState(Qt.Checked if self.__plot_data__[key].visible else Qt.Unchecked)
            self.__legend_model__.appendRow(item)
        self.redraw()

    def __init__(self, *plots):
        super().__init__()
        self.__plot_data__ = {}
        self.__plot_widget__ = gl.GLViewWidget()
        self.__legend_widget__ = QListView()

        vbox = QVBoxLayout(self)
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(self.__plot_widget__)
        splitter.addWidget(self.__legend_widget__)
        vbox.addWidget(splitter)

        self.__legend_model__ = QStandardItemModel()
        self.__legend_widget__.setModel(self.__legend_model__)
        self.__legend_model__.itemChanged.connect(self.legend_clicked)

        if len(plots) > 0:
            for plot in plots:
                self.add_plot(plot)
            self.refresh()

    def legend_clicked(self, item):
        name = item.text()
        plot_info = self.__plot_data__[name]
        if item.checkState() == Qt.Checked:
            plot_info.visible = True
        else:
            plot_info.visible = False
        self.redraw()

    def redraw(self):
        pw = self.__plot_widget__
        pw.items.clear()

        for key in self.__plot_data__:
            plot_info = self.__plot_data__[key]
            if plot_info.visible and (len(plot_info.xs) > 0 and len(plot_info.ys) > 0):
                pi = gl.GLSurfacePlotItem(x=plot_info.xs, y=plot_info.ys, z=plot_info.zs, color=plot_info.color, shader='shaded')
                pw.addItem(pi)
        pw.update()


import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    multi_plot = MultiPlot3d()
    multi_plot.show()

    multi_plot.add_plot('Plot1')
    multi_plot.add_plot('Plot2', description='Super plot')

    multi_plot.set_plot_data('Plot1', xs=np.array([0, 1, 2]), ys=np.array([0, 1, 2]), zs=np.array([[1, 3, 5], [4, 6, 3], [4, 1, 2]]))
    multi_plot.set_plot_data('Plot2', xs=np.array([0, 1, 2]), ys=np.array([0, 1, 2]), zs=np.array([[8, 6, 5], [4, 6, 2], [3, 1, 0]]))

    multi_plot.refresh()


    sys.exit(app.exec_())