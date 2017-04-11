from abc import ABC, abstractmethod
from typing import List, Set, Dict


# Model
class Node:
    def __init__(self):
        self.id: int = None
        self.arguments: Dict[NodeArgument] = {}  # {name : InputConnection}
        self.results: Dict[NodeResult] = {}  # {name : OutputConnection}

        self.function: Function = None  # Function
        self.display_function: Function = None  # Function
        self.import_modules: List[str] = []  # [String], example: ['import numpy as np']

    def get_argument(self, name: str):
        return self.arguments[name]

    def get_result(self, name: str):
        return self.results[name]

    def add_argument(self, name):
        if

    @staticmethod
    def connect(result: NodeResult, argument: NodeArgument):
        if argument.in_value is None:
            argument.in_value = result
            result.targets.add(argument)

    @staticmethod
    def disconnect(result: NodeResult, argument: NodeArgument):
        if argument.in_value == result and argument in result.targets:
            argument.in_value = None
            result.targets.remove(argument)


class Function(ABC):
    @abstractmethod
    def compute(self, input_connections, output_connections):
        pass


class NodeArgument:
    def __init__(self):
        self.name: str = None
        self.node: Node = None
        self.in_value: NodeResult = None


class NodeResult:
    def __init__(self):
        self.name: str = None
        self.node: Node = None
        self.value = None
        self.targets: Set[NodeArgument] = {}


if __name__ == "__main__":
    print("HELLO!")
