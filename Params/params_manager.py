import yaml

class ParamsManager:

    def __init__(self, params_path):
        self.params_path = params_path
        self.params = self.load_params()

    def load_params(self):

        with open(self.params_path, 'r') as f:
            params = yaml.safe_load(f)

        return params
   
    def get_params(self):
        return self.params

    def get_param(self, param_name):
        return self.params[param_name]

    def set_param(self, param_name, param_value):
        self.params[param_name] = param_value

    def store_params(self):
        with open(self.params_path, 'w') as f:
            yaml.dump(self.params, f)

    def print_params(self):
        print(self.params)

    def print_param(self, param_name):

        print(self.params[param_name])

