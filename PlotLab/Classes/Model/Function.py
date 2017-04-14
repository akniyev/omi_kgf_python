import textwrap
from typing import List

from PlotLab.Classes.Model.NodeArgument import NodeArgument
from PlotLab.Classes.Model.NodeResult import NodeResult


class Function:
    # CLASS:
    # @staticmethod
    # class NodeFunction:
    #     def compute_values(self, values):
    #         pass

    def __init__(self):
        self.counter = 0
        self.function_name = ""
        self.function_body = ""

    def get_next_counter(self):
        self.counter += 1
        return self.counter

    def compute(self, arguments: List[NodeArgument], results: List[NodeResult]):
        num = self.get_next_counter()
        fun_name = "Node{}{}".format(self.function_name, num)
        body = textwrap.indent(self.function_body, "  ")
        body = "class {}:\n".format(fun_name) + body
        values = {}
        for argument in arguments:
            values[argument.name] = argument.in_value.value
        f_call = "{}.compute_values(values)".format(fun_name)
        exec(body)
        computed_result = eval(f_call)
        for node_result in results:
            if node_result.name not in computed_result:
                return False

        for node_result in results:
            node_result.value = computed_result[node_result.name]

        return True