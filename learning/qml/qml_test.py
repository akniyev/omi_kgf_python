import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout


def on_resize(sender):
    print("resize")

# Main Function
if __name__ == '__main__':
    # Create main app
    app = QApplication(sys.argv)
    # Create a label and set its properties

    w_settings = QQuickView()
    w_settings.setSource(QUrl('settings_window.qml'))

    w_settings.show()


    sys.exit(app.exec_())