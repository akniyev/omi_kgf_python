from PlotLab.Classes.Model import Node
from PlotLab.Classes.Model.NodeResult import NodeResult


class NodeArgument:
    def __init__(self):
        self.name: str = None
        self.node: Node = None
        self.in_value: NodeResult = None