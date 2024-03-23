"""
Uart Command Instances
"""

from .format.command import CommandBuilder
from .format.parameter import Parameter, ParamType
from .format.checker import IntChecker, FloatChecker, EnumChecker
from .enums import ModeEnum, LineColorEnum, MarkerColorEnum, CameraEvEnum


# 参考 https://robomaster-dev.readthedocs.io/zh-cn/latest/text_sdk/protocol_api.html


class SdkCtrl:
    enterSdk = CommandBuilder('command')
    quitSdk = CommandBuilder('quit')


class Robot:
    setMode = CommandBuilder('robot mode', [Parameter('mode', ModeEnum.free, EnumChecker(ModeEnum))])
    getMode = CommandBuilder('robot mode ?')
    getBattery = CommandBuilder('robot battery ?')


class ChassisCtrl:
    setSpeed = CommandBuilder('chassis speed', [
        Parameter('x', 0, FloatChecker(-3.5, 3.5), ParamType.value_and_key),
        Parameter('y', 0, FloatChecker(-3.5, 3.5), ParamType.value_and_key),
        Parameter('z', 0, FloatChecker(-600, 600), ParamType.value_and_key),
    ])
    setWheel = CommandBuilder('chassis wheel', [
        Parameter('w1', 0, IntChecker(-1000, 1000), ParamType.value_and_key),
        Parameter('w2', 0, IntChecker(-1000, 1000), ParamType.value_and_key),
        Parameter('w3', 0, IntChecker(-1000, 1000), ParamType.value_and_key),
        Parameter('w4', 0, IntChecker(-1000, 1000), ParamType.value_and_key),
    ])
    setMove = CommandBuilder('chassis move', [
        Parameter('x', 0, FloatChecker(-3.5, 3.5), ParamType.value_and_key),
        Parameter('y', 0, FloatChecker(-3.5, 3.5), ParamType.value_and_key),
        Parameter('z', 0, FloatChecker(-1800, 1800), ParamType.value_and_key),
    ])
    getSpeed = CommandBuilder('chassis speed ?')
    getPosition = CommandBuilder('chassis position ?')
    getAttitude = CommandBuilder('chassis attitude ?')
    getStatus = CommandBuilder('chassis status ?')
    setPush = CommandBuilder('chassis push', [Parameter('args', '')])


class GimbalCtrl:
    setSpeed = CommandBuilder('gimbal speed', [
        Parameter('p', 0, FloatChecker(-450, 450), ParamType.value_and_key),
        Parameter('y', 0, FloatChecker(-450, 450), ParamType.value_and_key),
    ])
    setMove = CommandBuilder('gimbal move', [
        Parameter('p', 0, FloatChecker(-55, 55), ParamType.value_and_key),
        Parameter('y', 0, FloatChecker(-55, 55), ParamType.value_and_key),
        Parameter('vp', 1, IntChecker(0, 540), ParamType.value_and_key),
        Parameter('vy', 1, IntChecker(0, 540), ParamType.value_and_key),
    ])
    setMoveTo = CommandBuilder('gimbal moveto', [
        Parameter('p', 0, FloatChecker(-25, 30), ParamType.value_and_key),
        Parameter('y', 0, FloatChecker(-250, 250), ParamType.value_and_key),
        Parameter('vp', 1, IntChecker(0, 540), ParamType.value_and_key),
        Parameter('vy', 1, IntChecker(0, 540), ParamType.value_and_key),
    ])
    setSuspend = CommandBuilder('gimbal suspend')
    setResume = CommandBuilder('gimbal resume')
    setRecenter = CommandBuilder('gimbal recenter')
    getAttitude = CommandBuilder('gimbal attitude ?')
    setPush = CommandBuilder('gimbal push', [Parameter('args', '')])


class BlasterCtrl:
    setBead = CommandBuilder('blaster bead', [Parameter('num', 1, IntChecker(1, 5))])
    setFire = CommandBuilder('blaster fire')
    getBead = CommandBuilder('blaster bead ?')


class ArmorCtrl:
    # TODO
    pass


class SoundCtrl:
    # TODO
    pass


class PwmCtrl:
    setValue = CommandBuilder('pwm value', [
        Parameter('port_mask', 0, IntChecker(0, 0xffff)),
        Parameter('value', 12.5, FloatChecker(0, 100)),
    ])
    setFreq = CommandBuilder('pwm freq', [
        Parameter('port_mask', 0, IntChecker(0, 0xffff)),
        Parameter('value', 1000, IntChecker(0, 10000)),
    ])


class LedCtrl:
    # TODO
    pass


class SensorAdapterCtrl:
    # TODO
    pass


class IrDistanceSensorCtrl:
    # TODO
    pass


class ServoCtrl:
    setAngle = CommandBuilder('servo angle', [
        Parameter('id', 1, IntChecker(1, 3), ParamType.value_and_key),
        Parameter('angle', 0, FloatChecker(-180, 180), ParamType.value_and_key),
    ])
    setSpeed = CommandBuilder('servo speed', [
        Parameter('id', 1, IntChecker(1, 3), ParamType.value_and_key),
        Parameter('speed', 0, FloatChecker(-1800, 1800), ParamType.value_and_key),
    ])
    setStop = CommandBuilder('servo stop')
    getAngle = CommandBuilder('servo angle', [
        Parameter('id', 1, IntChecker(1, 3)),
        Parameter('?', None, param_type=ParamType.key_only),
    ])


class RoboticArmCtrl:
    setMove = CommandBuilder('robotic_arm move', [
        Parameter('x', 0, FloatChecker(-100, 100), ParamType.value_and_key),
        Parameter('y', 0, FloatChecker(-100, 100), ParamType.value_and_key),
    ])
    setMoveTo = CommandBuilder('robotic_arm moveto', [
        Parameter('x', 0, FloatChecker(-100, 100), ParamType.value_and_key),
        Parameter('y', 0, FloatChecker(-100, 100), ParamType.value_and_key),
    ])
    setRecenter = CommandBuilder('robotic_arm recenter')
    setStop = CommandBuilder('robotic_arm stop')
    getPosition = CommandBuilder('robotic_arm position ?')


class RoboticGripperCtrl:
    setOpen = CommandBuilder('robotic_gripper open', [
        Parameter('level', 1, IntChecker(1, 4)),
    ])
    setClose = CommandBuilder('robotic_gripper close', [
        Parameter('level', 1, IntChecker(1, 4)),
    ])
    getStatus = CommandBuilder('robotic_gripper status ?')


class AiCtrl:
    setAttributeLine = CommandBuilder('AI attribute', [
        Parameter('line_color', LineColorEnum.red, EnumChecker(LineColorEnum), ParamType.value_and_key),
    ])
    setAttributeMarker = CommandBuilder('AI attribute', [
        Parameter('marker_color', MarkerColorEnum.red, EnumChecker(MarkerColorEnum), ParamType.value_and_key),
    ])
    setAttributeMarkerDist = CommandBuilder('AI attribute', [
        Parameter('marker_dist', 0.5, FloatChecker(0.5, 3), ParamType.value_and_key),
    ])
    setPush = CommandBuilder('AI push', [Parameter('args', '')])


class CameraCtrl:
    setExposure = CommandBuilder('camera exposure', [
        Parameter('ev_level', CameraEvEnum.small, EnumChecker(CameraEvEnum)),
    ])


class StreamCtrl:
    setOn = CommandBuilder('stream on')
    setOff = CommandBuilder('stream off')


class AudioCtrl:
    setOn = CommandBuilder('audio on')
    setOff = CommandBuilder('audio off')


class GameMsgCtrl:
    setOn = CommandBuilder('game_msg on')
    setOff = CommandBuilder('game_msg off')
