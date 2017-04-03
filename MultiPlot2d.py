from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import pyqtgraph as pg


class PlotInfo:
    def __init__(self, name, description=""):
        super().__init__()
        self.name = name
        self.description = description

    name = ""
    description = ""
    xs = []
    ys = []
    plot = 0


class MultiPlot2d(QWidget):
    def add_plot(self, name, description=""):
        if name in self.__plot_data__:
            print('Plot with this name already exists!')
            return
        self.__plot_data__[name] = PlotInfo(name, description)

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
                description = plot_info[0]
            plot_info.description = description
            plot_info.xs = xs
            plot_info.ys = ys
        else:
            print('No plot with this name')

    def clear_plot_data(self, name):
        if name in self.__plot_data__:
            plot_info = self.__plot_data__[name]
            plot_info[1] = []
            plot_info[2] = []
        else:
            print('No plot with this name')

    def refresh(self):
        self.__legend_model__.clear()
        for key in self.__plot_data__:
            item = QStandardItem()
            description = self.__plot_data__[key].description
            item.setText(key + (' (' + description + ')' if description != "" else ""))
            item.setCheckable(True)
            item.setCheckState(Qt.Checked)
            self.__legend_model__.appendRow(item)
        self.redraw()

    __plot_data__ = {}

    def __init__(self):
        super().__init__()
        self.__plot_widget__ = pg.PlotWidget()
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

    def legend_clicked(self, item):
        self.redraw()

    def redraw(self):
        pw = self.__plot_widget__
        pw.


import sys

app = QApplication(sys.argv)

multi_plot = MultiPlot2d()
multi_plot.show()

multi_plot.add_plot('Plot1')
multi_plot.add_plot('Plot2', 'Super plot')

multi_plot.refresh()


sys.exit(app.exec_())








