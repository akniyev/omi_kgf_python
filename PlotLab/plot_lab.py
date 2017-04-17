import sys
from random import random, randint

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import *

from PlotLab.Classes.View.BoxDiagramItem import BoxDiagramItem
from PlotLab.Classes.View.DiagramWidget import DiagramWidget
from PlotLab.Classes.View.NodeItem import NodeItem

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # v = SchemeWidget()
    #
    #
    # v.show()

    # for i in range(10):
    #     c = DraggableWidget()
    #     #c.setGeometry(10, 10, 50, 50)
    #     c.drag_area = QRect(0, 0, 25, 25)
    #     v.scene().addWidget(c)

    # node_widget = OldDiagramWidget()
    # node_widget.show()

    dw = DiagramWidget()
    dw.show()
    bdi = BoxDiagramItem()

    dw.add_diagram_item(bdi)
    for i in range(4):
        ni = NodeItem()
        ni.center = QPoint(randint(1, 400), randint(1, 400))
        dw.add_diagram_item(ni)
        ni.set_node_inputs('x', 'y', 'z')
        ni.set_node_outputs('a')

    sys.exit(app.exec_())

#     n1 = Node()
#     n2 = Node()
#     n1.add_result('a')
#     n2.add_argument('x')
#     n2.add_argument('y')
#     Node.connect(n1.get_result('a'), n2.get_argument('x'))
#     Node.connect(n1.get_result('a'), n2.get_argument('y'))
#     # Node.disconnect(n1.get_result('a'), n2.get_argument('x'))
#     n1.set_results('a', 'b', 'c')
#     n2.set_arguments('x', 'z')
#     n3 = Node()
#     n3.set_results('a')
#
#     n3.function = ConstantFunction(2, "Constant2")
#
#     n4 = Node()
#     n4.set_arguments('x')
#     n4.set_results('b')
#     f2 = Function()
#     f2.function_name = "Square"
#     f2.function_body = """@staticmethod
# def compute_values(values):
#     x = values['x']
#     return { 'b' : x * x }
# """
#     n4.function = SimpleFunction({'b': 'x * x * x'}, "Simplefunction")
#     Node.connect(n3.get_result('a'), n4.get_argument('x'))
#     n3.compute()
#     n4.compute()
