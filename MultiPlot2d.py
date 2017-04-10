from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from random import randrange


class PlotInfo:
    def __init__(self, name, color, description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.visible = True
        self.color = color

    name = ""
    description = ""
    xs = []
    ys = []
    plot = 0


class MultiPlot2d(QWidget):
    def add_plot(self, name, color=0, description=""):
        if color == 0:
            color = (randrange(0, 255), randrange(0, 255), randrange(0, 255), 255)
        if name in self.__plot_data__:
            print('Plot with this name already exists!')
            return
        self.__plot_data__[name] = PlotInfo(name, color, description)

    def remove_plot(self, name):
        if name in self.__plot_data__:
            del self.__plot_data__[name]

    def get_plot_names(self):
        """ get_plot_names() -> [String]"""
        return self.__plot_data__.keys()

    def get_plot_info(self, name):
        """ get_plot_info(name) -> PlotInfo"""
        self.__plot_data__[name]

    def set_plot_data(self, name, xs, ys, description=""):
        if name in self.__plot_data__ and len(xs) == len(ys):
            plot_info = self.__plot_data__[name]
            if description == "":
                description = plot_info.description
            plot_info.description = description
            plot_info.xs = xs
            plot_info.ys = ys
        else:
            print('No plot with this name')

    def clear_plot_data(self, name):
        if name in self.__plot_data__:
            plot_info = self.__plot_data__[name]
            plot_info.xs = []
            plot_info.ys = []
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
        self.__plot_widget__ = pg.PlotWidget()
        self.__legend_widget__ = QListView()
        # self.__plot_widget__.setBackground((255, 255, 255))

        vbox = QVBoxLayout(self)
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(self.__plot_widget__)
        splitter.addWidget(self.__legend_widget__)
        self.__legend_widget__.setGeometry(0, 0, 0, 100)
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
        pw.clear()

        for key in self.__plot_data__:
            plot_info = self.__plot_data__[key]
            if plot_info.visible:
                pi = pg.PlotDataItem()

                pw.addItem(pi)
                print(plot_info.color)
                pi.setData(x=plot_info.xs, y=plot_info.ys, pen=plot_info.color)

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    multi_plot = MultiPlot2d()
    multi_plot.show()

    multi_plot.add_plot('Plot1')
    multi_plot.add_plot('Plot2', description='Super plot')

    multi_plot.set_plot_data('Plot1', [1, 2, 3, 4, 5], [1, 2, 1, 2, 1])
    multi_plot.set_plot_data('Plot2', [1, 2, 3, 4, 5], [-1, -2, -1, 2, 10])

    multi_plot.refresh()


    sys.exit(app.exec_())








