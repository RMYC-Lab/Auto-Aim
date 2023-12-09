import math


class MarkerTarget():
    def __init__(self, x: int = 0, y: int = 0, z: float = 0,
                 center_x: int = 0, center_y: int = 0,
                 error_w: float = 0, error_h: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.center_x = center_x
        self.center_y = center_y
        self.error_w = error_w
        self.error_h = error_h

    def set_position(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def is_shootable(self):
        return self.center_x - self.error_h / 2 < self.x < self.center_x + self.error_h / 2 and \
               self.center_y - self.error_w / 2 < self.y < self.center_y + self.error_w / 2

    def get_x_error(self):
        return self.x - self.center_x

    def get_y_error(self):
        return self.y - self.center_y

    def get_center_distance(self):
        return math.sqrt(self.get_x_error() ** 2 + self.get_y_error() ** 2)
