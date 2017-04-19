from PlotLab.Classes.View.DiagramItem import DiagramItem
from PlotLab.Classes.View.NodeItem import NodeItem


class PlotItem2d(NodeItem):
    def __init__(self):
        super().__init__()
        self.set_node_inputs(['x', 'y'])
        self.set_node_outputs([])
        self.name = "Plot2d"
        from PlotLab.Classes.View.Widgets.MultiPlotWidget2d import MultiPlotWidget2d
        self.plot: MultiPlotWidget2d = None

    def invalidate_node(self):
        super().invalidate_node()
        if self.plot is not None:
            self.plot.set_plot_data('default', [], [])
            self.plot.refresh()

    def is_computed(self):
        return self.is_ready_to_compute()

    def is_result_computed(self):
        return False

    def is_sequence(self, arg):
        return (not hasattr(arg, "strip") and
                hasattr(arg, "__getitem__") or
                hasattr(arg, "__iter__"))

    def is_number(self, x):
        import numbers
        return isinstance(x, numbers.Number)

    def check_if_number_array(self, xs):
        if not self.is_sequence(xs):
            return False
        for i in xs:
            if not self.is_number(i):
                return False

        return True

    def compute(self):
        if self.plot is not None:
            if self.is_ready_to_compute():
                h0 = self.input_handlers[0]
                h1 = self.input_handlers[1]
                xs = h0.input_line.source.out_value
                ys = h1.input_line.source.out_value
                if self.check_if_number_array(xs) and self.check_if_number_array(ys):
                    self.plot.set_plot_data('default', xs, ys)
                self.plot.refresh()
            else:
                print("NO DATA!")
        else:
            print("NO PLOT!")

