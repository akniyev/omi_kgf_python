import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    for i in range(10):
        x = np.random.normal(loc=0.0, scale=2, size=100)
        pg.plot(x)
        #widget = pg.PlotWidget(title='Plot{}'.format(i))
        #widget.plotItem.plot(x)
        #widget.show()

    sys.exit(app.exec_())