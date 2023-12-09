# PID 控制器
# 参考 DJI RoboMaster Python SDK
# https://github.com/RMYC-Lab/RoboMaster-Python/blob/main/Decompile-decompyle3/src/test/rm_ctrl.py#L4205
import time


class PIDCtrl(object):
    """PID 控制器"""

    def __init__(self, kp=0.0, ki=0.0, kd=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.kp_item = 0
        self.ki_item = 0
        self.kd_item = 0
        self.error = 0
        self.last_error = 0
        self.last_time = 0

    def reset(self):
        self.kp_item = 0
        self.ki_item = 0
        self.kd_item = 0
        self.error = 0
        self.last_error = 0
        self.last_time = 0

    def set_ctrl_params(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_error(self, error):
        self.error = error

    def get_output(self):
        cur_time = time.time()
        if self.last_time == 0:
            self.last_time = cur_time
        else:
            dt = cur_time - self.last_time
            if dt > 0.2:
                self.ki_item = 0
            self.last_time = cur_time
            self.kp_item = self.kp * self.error
            self.ki_item = self.ki_item + 1 * self.ki * self.error
            self.kd_item = self.kd * (self.error - self.last_error) / 1
            self.last_error = self.error
        return self.kp_item + self.ki_item + self.kd_item
