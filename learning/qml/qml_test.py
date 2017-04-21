import sys
from PyQt5.QtCore import Qt, QUrl, QObject
from PyQt5.QtGui import QPainter
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickView, QQuickItem, QQuickPaintedItem
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton


def on_resize(sender):
    print("resize")

name_field: QQuickItem = None

def save_button_clicked(name):
    print('mouse clicked %s' % name)


class MyPaintedItem(QQuickPaintedItem):
    def __init__(self, parent: QQuickItem):
        super().__init__(parent)

    def paint(self, painter: QPainter):
        painter.drawEllipse(10, 10, 20, 20)


# Main Function
if __name__ == '__main__':
    # Create main app
    app = QApplication(sys.argv)
    # Create a label and set its properties

    qmlRegisterType(MyPaintedItem, 'MyPaintedItem', 1, 0, 'MyPaintedItem')

    w_settings = QQuickView()
    w_settings.setSource(QUrl('settings_window.qml'))
    w_settings.setResizeMode(QQuickView.SizeRootObjectToView)
    w_settings.show()

    # button_save: QQuickItem = w_settings.rootObject().findChild(QQuickItem, 'button_save')
    # button_reset: QQuickItem = w_settings.rootObject().findChild(QQuickItem, 'button_reset')
    # name_field = w_settings.rootObject().findChild(QQuickItem, 'name_field')
    # name_field.setProperty('text', 'Hello!')

    # button_save.pressed.connect(save_button_clicked)

    sys.exit(app.exec_())