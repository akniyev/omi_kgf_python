# Model
class Node:
    def __init__(self):
        self.id = None
        self.input_variables = {}
        self.output_variables = {}

        self.function_code = ""
        self.display_function_code = ""
        self.import_modules = []  # list of include strings


class Link:
    def __init__(self):
        self.start_node_id = None
        self.end_node_id = None
        self.start_output_name = None
        self.end_input_name = None


class Plot:
    def __init__(self):
        self.nodes = []
        self.links = []
        self.nodes_coordinates = {}  # {id : (x, y)}

    def add_node(self, node, id):
        node.id = id
        self.nodes.append(node)
        return True

    def add_link(self, start_node_id, start_output_name, end_node_id, end_input_name):
        # check: in, out nodes exist
        # check: in, out nodes have such values
        # check: out_value1 and in_value2 not occupied
        link = Link()
        link.start_node_id = start_node_id
        link.end_node_id = end_node_id
        link.start_output_name = start_output_name
        link.end_input_name = end_input_name
        self.links.append(link)
        return True




