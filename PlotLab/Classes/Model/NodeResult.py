from typing import Set


class NodeResult:
    def __init__(self):
        self.name: str = None
        self.node: Node = None
        self.value = None
        self.targets: Set[NodeArgument] = set()