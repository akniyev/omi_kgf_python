import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
import pyqtgraph as pg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = loadUi('firstgui.ui')
    widget.show()

    plot = pg.PlotWidget()
    plot.plotItem.plot([1, 2, 3, 4, 5])

    plot.show()

    sys.exit(app.exec_())