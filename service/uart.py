# import serial
from robot_ctrl.uart.uart import UartProtocol
from robot_ctrl.uart.format.command import Command
from robot_ctrl.uart.commands import SdkCtrl
from multiprocessing import Process, Queue


class UartRobotCtrl():
    def __init__(self, port: str):
        self._uart = UartProtocol(port)

    def connect(self, try_times: int = 3):
        self._uart.open()
        for _ in range(try_times):
            recv = self.send(SdkCtrl.enterSdk.build(), False, 5)  # 进入串口控制模式
            if recv == 'ok' or recv == 'Already in SDK mode':
                return True
        return False

    '''
    def gimbal_speed(self, pitch_speed: float, yaw_speed: float):
        """控制云台运动速度

        Args:
            pitch_speed (float): pitch 轴速度，单位 °/s
            yaw_speed (float): yaw 轴速度，单位 °/s
        """
        self.send(f'gimbal speed p {pitch_speed:.2f} y {yaw_speed:.2f};')
        # return self.recv()

    def gimbal_move(self, pitch_degree: float, yaw_degree: float, pitch_speed, yaw_speed):
        """控制云台运动到指定位置，坐标轴原点为当前位置

        Args:
            pitch_degree (float): pitch 轴角度，单位 °
            yaw_degree (float): yaw 轴角度，单位 °
            pitch_speed (float): pitch 轴运动速度，单位 °/s
            yaw_speed (float): yaw 轴运动速度，单位 °/s
        """
        self.send(f'gimbal move p {pitch_degree:.2f} y {yaw_degree:.2f} vp {pitch_speed:.2f} vy {yaw_speed:.2f};')
        # return self.recv()

    def set_blaster_bead(self, num: int):
        """设置发射珠子数量

        Args:
            num (int): 珠子数量
        """
        self.send(f'blaster bead {num};')
        # return self.recv()

    def blaster_fire(self):
        """发射珠子"""
        self.send('blaster fire;')
        # return self.recv()

    def get_gimbal_attitude(self):
        """获取云台姿态信息

        Returns:
            str: 云台当前姿态，格式为 pitch_degree, yaw_degree;
        """
        self.send('gimbal attitude ?;')
        return [float(i) for i in self.recv().split(' ')]

    def set_robot_mode(self, mode: str):
        """设置机器人模式

        Args:
            mode (str): chassis_lead : 云台跟随底盘模式
                        gimbal_lead : 底盘跟随云台模式
                        free : 自由模式
        """
        self.send(f'robot mode {mode};')
        # return self.recv()

    def open_gimabal_push(self):
        """打开云台推送"""
        self.send('gimbal push attitude on;')
        # return self.recv()

    def gimbal_recenter(self):
        """云台回中"""
        self.send('gimbal recenter;')
        # return self.recv()

    def disconnect(self):
        self.serial.close()
    '''

    def send(self, cmd: Command, ignore_res: bool = True, timeout: float = 1):
        return self._uart.send(cmd, ignore_res, timeout)

    # def send(self, msg: str):
    #     if not msg.endswith(';'):
    #         msg += ';'
    #     print('Uart send:', msg)
    #     self.serial.write(msg.encode('utf-8'))

    # def recv(self):
    #     recv_txt = self.serial.readall().decode('utf-8')
    #     if recv_txt.endswith(';\n'):
    #         recv_txt = recv_txt[:-2]
    #     print('Uart recv:', recv_txt)
    #     return recv_txt


