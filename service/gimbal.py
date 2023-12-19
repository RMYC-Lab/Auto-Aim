import multiprocessing as mp
from structure.marker_target import MarkerTarget
from service.uart import UartRobotCtrl
from utils.pid import PIDCtrl

class GimbalTask(mp.Process):
    def __init__(self, robot: UartRobotCtrl, x_pid: PIDCtrl, y_pid: PIDCtrl):
        super().__init__()
        self.robot = robot
        self.target_qunue = []
        self.last_shoot_time = 0
        self.x_pid = x_pid
        self.y_pid = y_pid

    def run(self):
        while True:
            if len(self.target_qunue) > 0:
                # 排列列表 获取最近的目标
                self.target_qunue.sort(key=lambda target: target.get_center_distance())
                target = self.target_qunue[0]
                x_error = target.get_x_error()
                y_error = target.get_y_error()
                # 计算PID
                self.x_pid.set_error(x_error)
                self.y_pid.set_error(y_error)
                x_output = int(self.x_pid.get_output())
                y_output = int(self.y_pid.get_output())
                if target.is_shootable():
                    self.shoot()
                else:
                    self.robot.set_gimbal_speed(x_output, y_output)

                


    def add_target(self, target: MarkerTarget):
        self.target_qunue.append(target)

    def clear_target(self):
        self.target_qunue.clear()

    def shoot(self):
        
