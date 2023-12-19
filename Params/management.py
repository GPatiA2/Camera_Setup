import yaml

class ParamsManager:

    def __init__(self, params_path):
        self.params_path = params_path
        self.params = self.load_params()

    def load_params(self):

        with open(self.params_path, 'r') as f:
            params = yaml.safe_load(f)

        if params is None:
            params = {}

        return params
   
    def get_camera_params(self, cam_name):
        return self.params[cam_name]

    def get_camera_matrix(self, cam_name):
        return self.params[cam_name]['camera_matrix']

    def get_distortion_coefs(self, cam_name):
        return self.params[cam_name]['distortion_coefs']

    def store_camera_params(self, params):
        self.params[params['cam_name']] = params

    def save_params(self):
        with open(self.params_path, 'w') as f:
            yaml.dump(self.params, f)
