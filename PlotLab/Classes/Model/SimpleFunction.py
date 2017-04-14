from typing import Dict, List

from PlotLab.Classes.Model.Function import Function
from PlotLab.Classes.Model.NodeArgument import NodeArgument
from PlotLab.Classes.Model.NodeResult import NodeResult


class SimpleFunction(Function):
    def __init__(self, expressions: Dict[str, str], name: str): # SimpleFunction({'b': 'x * x * x'}, "Simplefunction")
        super().__init__()
        self.function_name = name
        self.function_body = expressions

    def compute(self, arguments: List[NodeArgument], results: List[NodeResult]):
        values = {}
        expressions: Dict[str, str] = self.function_body
        for argument in arguments:
            values[argument.name] = argument.in_value.value
        computed_result = {}
        for arg_name in expressions.keys():
            arg_value = eval(expressions[arg_name], values)
            computed_result[arg_name] = arg_value
        for node_result in results:
            node_result.value = computed_result[node_result.name]

        return True