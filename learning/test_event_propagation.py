import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import QApplication, QWidget


class Filter(QtCore.QObject):
    def __init__(self):
        super().__init__()

    def eventFilter(self, obj, event):
        print(event.type())
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    filter = Filter()
    widget.installEventFilter(filter)
    widget.show()
    sys.exit(app.exec_())