from PlotLab.Classes.Model.Function import Function


class ConstantFunction(Function):
    def __init__(self, value, name: str):
        super().__init__()
        self.function_body = ("@staticmethod\n"
                              "def compute_values(values):\n"
                              "  return {'a': 2}")
        self.function_name = name