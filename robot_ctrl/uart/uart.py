"""
UART protocol implementation
串口协议实现
"""
import re
import serial
import queue
import time
import threading

from typing import Union

from .format.command import Command

DEFAULT_BAUDRATE = 115200
DEFAULT_BYTESIZE = serial.EIGHTBITS
DEFAULT_STOPBITS = serial.STOPBITS_ONE
DEFAULT_PARITY = serial.PARITY_NONE
DEFAULT_TIMEOUT = 0.2


class UartProtocolBase():
    """
    Uart protocol base class
    实现基本的串口通讯
    """
    def __init__(self, port: str,
                 baudrate: int = DEFAULT_BAUDRATE,
                 bytesize: int = DEFAULT_BYTESIZE,
                 stopbits: int = DEFAULT_STOPBITS,
                 parity: str = DEFAULT_PARITY,
                 timeout: float = DEFAULT_TIMEOUT) -> None:
        self._uart = serial.Serial()
        self._uart.port = port
        self._uart.baudrate = baudrate
        self._uart.bytesize = bytesize
        self._uart.stopbits = stopbits
        self._uart.parity = parity
        self._uart.timeout = timeout

    def send(self, msg: str) -> None:
        """
        Send message to the serial port
        发送消息到串口
        """
        self._uart.write(msg.encode('utf-8'))

    def recv(self) -> str:
        """
        Receive message from the serial port
        从串口接收消息
        """
        # return self._uart.readline().decode('utf-8')
        return self._uart.read_until(b';').decode('utf-8')  # 读取到分号结束

    def open(self) -> None:
        """
        Connect to the serial port
        连接到串口
        """
        self._uart.open()

    def close(self) -> None:
        """
        Disconnect from the serial port
        从串口断开连接
        """
        self._uart.close()


class UartProtocol:
    """
    Uart protocol class
    串口协议类
    """
    RES_REGEX = r'^(?P<result>.+?)( seq (?P<seq>.+))?;\n?$'
    GET_RES_INTERVAL = 0.05

    def __init__(self, port: str,
                 baudrate: int = DEFAULT_BAUDRATE,
                 bytesize: int = DEFAULT_BYTESIZE,
                 stopbits: int = DEFAULT_STOPBITS,
                 parity: str = DEFAULT_PARITY,
                 timeout: float = DEFAULT_TIMEOUT) -> None:
        # 使用 UartProtocolBase 作为底层通讯
        self._uart = UartProtocolBase(port, baudrate, bytesize, stopbits, parity, timeout)
        # 使用 queue.Queue 作为消息队列
        self._cmd_queue = queue.Queue()
        # 使用 queue.LifoQueue 作为响应队列 (后进先出)
        self._res_queue = queue.LifoQueue()
        # 忽略消息 seq 列表
        self._ignore_seq = []
        self._ignore_seq_lock = threading.Lock()
        # 定义线程停止标志
        self._stop_event = threading.Event()
        # 定义线程
        self._uart_recv_thread = threading.Thread(target=self._uart_recv_task)
        self._uart_send_thread = threading.Thread(target=self._uart_send_task)
        self.__open = False

    def open(self):
        """
        Connect to the serial port
        连接到串口
        """
        if not self._uart._uart.is_open:
            self._uart.open()
        if not self.__open:
            # 启动线程
            self._stop_event.clear()
            self._uart_recv_thread.start()
            self._uart_send_thread.start()
        # 清空消息队列
        while not self._cmd_queue.empty():
            self._cmd_queue.get()
        # 清空响应队列
        while not self._res_queue.empty():
            self._res_queue.get()
        self.__open = True

    def close(self):
        """
        Disconnect from the serial port
        从串口断开连接
        """
        if self.__open:
            # 设置停止标志
            self._stop_event.set()
            # 等待线程结束
            self._uart_recv_thread.join()
            self._uart_send_thread.join()
            self._uart.close()
            # 清空消息队列
            while not self._cmd_queue.empty():
                self._cmd_queue.get()
            # 清空响应队列
            while not self._res_queue.empty():
                self._res_queue.get()
            self.__open = False

    def send(self, cmd: Command, ignore_res: bool = True, timeout: float = 1) -> Union[str, None]:
        """
        Send command to the serial port
        发送命令到串口
        """
        # 生成消息
        msg, seq = cmd.format()
        # 判断是否忽略响应
        if ignore_res:
            # 将 seq 加入忽略列表
            with self._ignore_seq_lock:
                self._ignore_seq.append(seq)
        # 将消息放入消息队列
        self._cmd_queue.put(msg)
        if ignore_res:
            return
        _begin_time = time.time()
        while time.time() - _begin_time < timeout:
            try:
                # 从响应队列获取响应
                res = self._res_queue.get_nowait()
                # 解析响应
                res = re.match(self.RES_REGEX, res)
                if res is None:
                    continue
                # 获取 seq
                res_seq = res.group('seq')
                # 判断 seq 是否为当前命令的 seq
                if res_seq == seq:
                    return res.group('result')
                else:
                    # 将响应放回响应队列
                    self._res_queue.put(res.group())
            except queue.Empty:
                continue
            time.sleep(self.GET_RES_INTERVAL)
        return None

    def _uart_recv_task(self):
        """
        UART receive thread
        串口接收线程
        """
        while not self._stop_event.is_set():
            # 从串口接收消息
            msg = self._uart.recv()
            # 解析消息
            res = re.match(self.RES_REGEX, msg)
            if res is not None:
                # 获取 seq
                seq = res.group('seq')
                # 判断 seq 是否在忽略列表中
                with self._ignore_seq_lock:
                    if seq in self._ignore_seq:
                        continue
                    self._ignore_seq.remove(seq)
                # 将消息放入响应队列
                self._res_queue.put(msg)
            # 将消息放入消息队列
            # self._msg_queue.put(msg)

    def _uart_send_task(self):
        """
        UART send thread
        串口发送线程
        """
        while not self._stop_event.is_set():
            # 从消息队列获取消息
            msg = self._cmd_queue.get()
            # 发送消息到串口
            self._uart.send(msg)
