from typing import Dict, List

from PlotLab.Classes.Model.Function import Function
from PlotLab.Classes.Model.NodeArgument import NodeArgument
from PlotLab.Classes.Model.NodeResult import NodeResult


class Node:
    def __init__(self):
        self.id: int = None
        self.arguments: Dict[str, NodeArgument] = {}  # {name : InputConnection}
        self.results: Dict[str, NodeResult] = {}  # {name : OutputConnection}

        self.function: Function = None  # Function
        self.display_function: Function = None  # Function
        self.import_modules: List[str] = []  # [String], example: ['import numpy as np']

    def can_compute(self):
        for arg in self.arguments.values():
            if arg.in_value.value is None:
                return False
        if self.function is None:
            return False
        return True

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

    def compute(self):
        if not self.can_compute():
            return False

        self.function.compute(list(self.arguments.values()), list(self.results.values()))
        return True

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
