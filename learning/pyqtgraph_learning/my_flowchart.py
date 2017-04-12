from PyQt5.QtWidgets import QApplication
from pyqtgraph.flowchart import Flowchart, sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fc = Flowchart()
    w = fc.widget()
    w1 = fc.nodes()

    w.show()

    sys.exit(app.exec_())
