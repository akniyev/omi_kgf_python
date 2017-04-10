from abc import ABC, abstractmethod
from typing import List


# Model
class Node:
    def __init__(self):
        self.id = None
        self.input_connections : List[InputConnection] = {}             # [name : InputConnection]
        self.output_connections : List[OutputConnection] = {}           # [name : OutputConnection]

        self.function : Function = None                                 # Function
        self.display_function : Function = None                         # Function
        self.import_modules : List[str] = []                            # [String], example: ['import numpy as np']

    def connect(self, out_connection_name : str, node, in_connection_name : str):
        node: Node = node  # for IDE hints
        out_connection = self.output_connections[out_connection_name]
        in_connection = node.input_connections[in_connection_name]

        if (out_connection is not None) and (in_connection is not None) and out_connection.target_connection is None and in_connection.input_connection is None:





class Function(ABC):
    @abstractmethod
    def compute(self, input_connections, output_connections):
        pass


class InputConnection:
    def __init__(self):
        self.name = None
        self.input_node = None
        self.input_connection = None


class OutputConnection:
    def __init__(self):
        self.name = None
        self.value = None
        self.target_nodes = []
        self.target_connection = None



class Coordinate:
    x = 0
    y = 0



if __name__ == "__main__":
    print("HELLO!")




