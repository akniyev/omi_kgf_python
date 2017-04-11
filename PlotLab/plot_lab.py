from abc import ABC, abstractmethod
from typing import List, Set, Dict


# Model
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
        self.targets: Set[NodeArgument] = set()


class Node:
    def __init__(self):
        self.id: int = None
        self.arguments: Dict[str, NodeArgument] = {}  # {name : InputConnection}
        self.results: Dict[str, NodeResult] = {}  # {name : OutputConnection}

        self.function: Function = None  # Function
        self.display_function: Function = None  # Function
        self.import_modules: List[str] = []  # [String], example: ['import numpy as np']

    def get_argument(self, name: str):
        if name in self.arguments.keys():
            return self.arguments[name]
        else:
            return None

    def get_result(self, name: str):
        if name in self.results.keys():
            return self.results[name]
        else:
            return None

    def add_argument(self, name):
        if name not in self.arguments.keys():
            na = NodeArgument()
            na.name = name
            na.node = self
            self.arguments[name] = na
        else:
            print('Element with name {} already exists!'.format(name))

    def remove_argument(self, name):
        if name in self.arguments:
            arg: NodeArgument = self.arguments[name]
            if arg.in_value is not None:
                if arg in arg.in_value.targets:
                    arg.in_value.targets.remove(arg)
            del self.arguments[name]
        else:
            print('No element with name {}'.format(name))

    def add_result(self, name):
        if name not in self.results.keys():
            nr = NodeResult()
            nr.name = name
            nr.node = self
            self.results[name] = nr

    def remove_result(self, name):
        if name in self.results.keys():
            res: NodeResult = self.results[name]
            for target in res.targets:
                target.in_value = None
            del self.results[name]
        else:
            print('No element with name {}'.format(name))

    def set_arguments(self, *names):
        arg_names = list(self.arguments.keys())
        for name in arg_names:
            if name not in names:
                self.remove_argument(name)

        for name in names:
            if self.get_argument(name) is None:
                self.add_argument(name)

    def set_results(self, *names):
        res_names = list(self.results.keys())
        for name in res_names:
            if name not in names:
                self.remove_result(name)

        for name in names:
            if self.get_result(name) is None:
                self.add_result(name)

    @staticmethod
    def connect(result: NodeResult, argument: NodeArgument):
        if argument.in_value is None:
            argument.in_value = result
            result.targets.add(argument)

    @staticmethod
    def disconnect(result: NodeResult, argument: NodeArgument):
        if argument.in_value == result and argument in result.targets:
            argument.in_value = None
            if argument in result.targets:
                result.targets.remove(argument)


if __name__ == "__main__":
    n1 = Node()
    n2 = Node()
    n1.add_result('a')
    n2.add_argument('x')
    n2.add_argument('y')
    Node.connect(n1.get_result('a'), n2.get_argument('x'))
    Node.connect(n1.get_result('a'), n2.get_argument('y'))
    # Node.disconnect(n1.get_result('a'), n2.get_argument('x'))
    n1.set_results('a', 'b', 'c')
    n2.set_arguments('x', 'z')

    print("HELLO!")
