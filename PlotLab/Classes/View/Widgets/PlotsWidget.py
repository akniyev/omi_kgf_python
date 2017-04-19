from typing import List, Dict

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from PlotLab.Classes.View.PlotItem2d import PlotItem2d
from PlotLab.Classes.View.Widgets.MultiPlotWidget2d import MultiPlotWidget2d


class PlotsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.tabWidget = QTabWidget()
        self.vbox.addWidget(self.tabWidget)
        self.plots: Dict[int, QWidget] = {}

    def set_tabs(self, tab_ids: List[int]):
        ids_to_add = []
        ids_to_delete = []
        for id in tab_ids:
            if id not in self.plots:
                ids_to_add.append(id)
        for id in self.plots:
            if id not in tab_ids:
                ids_to_delete.append(id)

        for id in ids_to_delete:
            self.remove_tab(id)
        for id in ids_to_add:
            self.add_tab(id)

    def remove_tab(self, id: int):
        if id not in self.plots:
            return
        for i in range(self.tabWidget.count()):
            if self.tabWidget.widget(i) == self.plots[id]:
                self.tabWidget.removeTab(i)
                break
        del self.plots[id]

    def add_tab(self, id):
        if id in self.plots:
            return
        plot = MultiPlotWidget2d()
        plot.add_plot('default')
        self.plots[id] = plot
        self.tabWidget.addTab(plot, "{}".format(id))

    def get_plot_widget_for_id(self, id):
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == "{}".format(id):
                return self.tabWidget.widget(i)
        return None


