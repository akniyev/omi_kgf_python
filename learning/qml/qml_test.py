import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication, QLabel

# Main Function
if __name__ == '__main__':
    # Create main app
    app = QApplication(sys.argv)
    # Create a label and set its properties

    appLabel = QQuickView()
    appLabel.setSource(QUrl('settings_window.qml'))

    appLabel.show()

    sys.exit(app.exec_())