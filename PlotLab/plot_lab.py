import sys
from PyQt5 import Qt
from PyQt5.Qt import *

from PyQt5.QtGui import QPaintEvent, QPainter
from PyQt5.QtWidgets import *
from PlotLab.Classes.View.DiagramWidget import DiagramWidget
from PlotLab.Classes.View.DraggableWidget import DraggableWidget
from PlotLab.Classes.View.SchemeWidget import SchemeWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    v = SchemeWidget()
    s = QGraphicsScene()
    v.setScene(s)

    v.show()

    for i in range(10):
        c = DraggableWidget()
        c.setGeometry(10, 10, 50, 50)
        # c.drag_area = QRect(0, 0, 25, 25)
        s.addWidget(c)

    node_widget = DiagramWidget()
    # node_widget.show()

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
