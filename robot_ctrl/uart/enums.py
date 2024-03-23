"""Enums for the protocol."""

from enum import Enum


__all__ = [
    "SwitchEnum",
    "ModeEnum",
    "ChassisPushAttrEnum",
    "GimbalPushAttrEnum",
    "ArmorEventAttrEnum",
    "SoundEventAttrEnum",
    "LedCompEnum",
    "LedEffectEnum",
    "LineColorEnum",
    "MarkerColorEnum",
    "AiPushAttrEnum",
    "AiPoseIdEnum",
    "AiMarkerIdEnum",
    "CameraEvEnum",
]


class SwitchEnum(Enum):
    on = "on"
    off = "off"


class ModeEnum(Enum):
    chassis_lead = "chassis_lead"
    gimbal_lead = "gimbal_lead"
    free = "free"


class ChassisPushAttrEnum(Enum):
    position = "position"
    attitude = "attitude"
    status = "status"


class GimbalPushAttrEnum(Enum):
    attitude = "attitude"


class ArmorEventAttrEnum(Enum):
    hit = "hit"


class SoundEventAttrEnum(Enum):
    applause = "applause"


class LedCompEnum(Enum):
    all = "all"
    top_all = "top_all"
    top_right = "top_right"
    top_left = "top_left"
    bottom_all = "bottom_all"
    bottom_front = "bottom_front"
    bottom_back = "bottom_back"
    bottom_left = "bottom_left"
    bottom_right = "bottom_right"


class LedEffectEnum(Enum):
    solid = "solid"
    off = "off"
    pulse = "pulse"
    blink = "blink"
    scrolling = "scrolling"


class LineColorEnum(Enum):
    red = "red"
    blue = "blue"
    green = "green"


class MarkerColorEnum(Enum):
    red = "red"
    blue = "blue"


class AiPushAttrEnum(Enum):
    person = "person"
    gesture = "gesture"
    line = "line"
    marker = "marker"
    robot = "robot"


class AiPoseIdEnum(Enum):
    v = 4
    v_reverse = 5
    take_photo = 6


class AiMarkerIdEnum(Enum):
    stop = 1
    left = 4
    right = 5
    forward = 6
    heart = 8
    zero = 10
    one = 11
    two = 12
    three = 13
    four = 14
    five = 15
    six = 16
    seven = 17
    eight = 18
    nine = 19
    a = 20
    b = 21
    c = 22
    d = 23
    e = 24
    f = 25
    g = 26
    h = 27
    i = 28
    j = 29
    k = 30
    l = 31  # noqa: E741
    m = 32
    n = 33
    o = 34
    p = 35
    q = 36
    r = 37
    s = 38
    t = 39
    u = 40
    v = 41
    w = 42
    x = 43
    y = 44
    z = 45


class CameraEvEnum(Enum):
    default = "default"
    small = "small"
    medium = "medium"
    large = "large"
