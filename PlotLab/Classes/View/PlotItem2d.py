from PlotLab.Classes.View.DiagramItem import DiagramItem
from PlotLab.Classes.View.NodeItem import NodeItem


class PlotItem2d(NodeItem):
    def __init__(self):
        super().__init__()
        self.set_node_inputs(['x', 'y'])
        self.set_node_outputs([])
        self.name = "Plot2d"

    def is_computed(self):
        return self.is_ready_to_compute()

    def is_result_computed(self):
        return False

    def compute(self):
        print("PLOT!")
