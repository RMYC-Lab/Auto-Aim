import math
from typing import Union

from utils.region import Region

CENTER_X = 0
CENTER_Y = 0
FULL_WIDTH = 640
FULL_HEIGHT = 480
shoot_region = None


class MarkerTarget():
    def __init__(self, x: int = 0, y: int = 0, z: float = 0,
                 w: float = 0, h: float = 0,
                 error_w: float = 0, error_h: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.error_w = error_w
        self.error_h = error_h

    def set_position(self, x: int = 0, y: int = 0, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def is_shootable(self, new_shoot_region: Union[Region, None] = None):
        # if shoot_region is None and new_shoot_region is None:
        #     return False
        if new_shoot_region is not None:
            return new_shoot_region.is_in_region(self.x, self.y)
        if shoot_region is None:
            return False
        return shoot_region.is_in_region(self.x, self.y)
        # marker_center_x = self.x + self.w / 2
        # marker_center_y = self.y + self.h / 2
        # return CENTER_X - self.error_h / 2 < marker_center_x < CENTER_X + self.error_h / 2 and \
        #        CENTER_Y - self.error_w / 2 < marker_center_y < CENTER_Y + self.error_w / 2

    def get_x_error(self):
        marker_center_x = self.x + self.w / 2
        return (marker_center_x - CENTER_X) / FULL_WIDTH

    def get_y_error(self):
        marker_center_y = self.y + self.h / 2
        return (CENTER_Y - marker_center_y) / FULL_HEIGHT

    def get_center_distance(self):
        return math.sqrt(self.get_x_error() ** 2 + self.get_y_error() ** 2)


def set_center(x: int, y: int):
    global CENTER_X, CENTER_Y
    CENTER_X = x
    CENTER_Y = y


def set_shoot_region(region: Region):
    global shoot_region
    shoot_region = region


def set_full_resolution(width: int, height: int):
    global FULL_WIDTH, FULL_HEIGHT
    FULL_WIDTH = width
    FULL_HEIGHT = height
