from abc import ABC, abstractmethod
from typing import List


# Model
class Node:
    def __init__(self):
        self.id = None
        self.input_connections : List[Connection] = []         # [Connection]
        self.output_connections : List[Connection] = []        # [Connection]

        self.function : Function = None                # Function
        self.display_function : Function = None        # Function
        self.import_modules : List[str] = []            # [String], example: ['import numpy as np']

    def __init__(self, input_connection_names : List[str], output_connection_names : List[str]):
        self.__init__()

        self.input_connections = Connection.generate_connection_list(input_connection_names)
        self.output_connections = Connection.generate_connection_list(output_connection_names)

    def clear_input_connections(self):
        self.input_connections = []

    @staticmethod
    def find_connection(connections, connection_name):
        for i in range(len(connections)):
            if connections[i].name == connection_name:
                return connections[i]
        return False

    @staticmethod
    def delete_connection(self, connections : List[Connection], connection_name : str):
        c = self.find_connection(connections, connection_name)
        if c:
            connections.remove(c)

    def delete_input_connection(self, connection_name : str):
        self.delete_connection(self.input_connections, connection_name)

    def delete_output_connection(self, connection_name : str):
        self.delete_connection(self.output_connections, connection_name)

    @staticmethod
    def add_connection(self, connections : List[Connection], connection_name : str):
        c = self.find_connection(connections, connection_name)
        if not c:
            c = Connection()
            c.name = connection_name
            connections.append(c)
        else:
            print('Connection with this name already exists!')

    def add_input_connection(self, connection_name : str):
        self.add_connection(self.input_connections, connection_name)

    def add_output_connections(self, connection_name):
        self.add_connection(self.output_connections, connection_name)

    def connection_exists(self, connections : List[Connection], connection_name : str):
        return not self.find_connection(connections, connection_name)

    def input_connection_exists(self, connection_name : str):
        return self.connection_exists(self.input_connections, connection_name)

    def output_connection_exists(self, connection_name : str):
        return self.connection_exists(self.output_connections, connection_name)


class Function(ABC):
    @abstractmethod
    def compute(self, input_connections, output_connections):
        pass


class Connection:
    def __init__(self):
        self.name = None
        self.value = None
        self.target_node = None
        self.target_connection = None

    @staticmethod
    def generate_connection_list(names : List[str]):
        result = []
        for name in names:
            connection = Connection()
            connection.name = name
            result.append(connection)

        return result


class Coordinate:
    x = 0
    y = 0


class Plot:
    def __init__(self):
        self.nodes = {}
        self._id = 0

    def next_id(self):
        self._id += 1
        return self._id

    def add_node(self, node: Node):
        node_id = self.next_id()
        node.id = node_id
        self.nodes[node_id] = node

    def remove_node_by_id(self, node_id):
        del self.nodes[node_id]

    def connect_nodes(self, ):








