from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import *

from PlotLab.Classes.View.DiagramWidget import DiagramWidget
from PlotLab.Classes.View.NodeItem import NodeItem


class NodeSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.WindowModal)

        self.node: NodeItem = None
        self.sender: DiagramWidget = None

        self.init_ui()

    def init_ui(self):
        # Creating widgets
        self.vbox = QVBoxLayout()
        self.ok_button = QPushButton("Save")
        self.cancel_button = QPushButton("Reset")
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.name_label = QLabel("Name")
        self.name_textedit = QLineEdit()
        self.arguments_label = QLabel("Arguments")
        self.arguments_textedit = QLineEdit()
        self.results_label = QLabel("Results")
        self.results_textedit = QLineEdit()
        self.function_body_label = QLabel("Function body")
        self.function_body_textedit = QTextEdit()
        self.setLayout(self.vbox)

        # Settings
        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(10)
        metrics = QFontMetrics(font)
        self.function_body_textedit.setFont(font)
        self.function_body_textedit.setTabStopWidth(2 * metrics.width(' '))
        self.function_body_textedit.setLineWrapMode(QTextEdit.NoWrap)

        # Adding widgets
        self.vbox.addWidget(self.name_label)
        self.vbox.addWidget(self.name_textedit)
        self.vbox.addWidget(self.arguments_label)
        self.vbox.addWidget(self.arguments_textedit)
        self.vbox.addWidget(self.results_label)
        self.vbox.addWidget(self.results_textedit)
        self.vbox.addWidget(self.function_body_label)
        self.vbox.addWidget(self.function_body_textedit)
        self.vbox.addLayout(self.button_layout)

        # Actions
        self.cancel_button.clicked.connect(self.reset_action)
        self.ok_button.clicked.connect(self.save_action)

    def load_node(self, node: NodeItem, sender: DiagramWidget):
        self.node = node
        self.sender = sender
        self.load_ui_from_node(node)

    def load_ui_from_node(self, node: NodeItem):
        self.name_textedit.setText(node.name)

        args_string = ""
        for arg in node.input_handlers:
            args_string += arg.name + " "
        self.arguments_textedit.setText(args_string)

        res_string = ""
        for res in node.output_handlers:
            res_string += res.name + " "
        self.results_textedit.setText(res_string)

        self.function_body_textedit.setText(node.function_body)

    def save_action(self, sender: DiagramWidget):
        if self.node is None:
            return
        self.node.name = self.name_textedit.text()

        input_names = self.arguments_textedit.text().split()
        self.node.set_node_inputs(input_names)

        output_names = self.results_textedit.text().split()
        self.node.set_node_outputs(output_names)

        self.node.function_body = self.function_body_textedit.toPlainText()

        self.sender.reload_graph()

    def reset_action(self, sender):
        if self.node is not None:
            self.load_ui_from_node(self.node)
