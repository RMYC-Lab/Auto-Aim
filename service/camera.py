from multiprocessing import Process, Queue
import cv2
import time


class CameraTask(Process):
    def __init__(self, img_queue: Queue, timeout: float = 2):
        super().__init__()
        self.img_queue = img_queue
        self.timeout = timeout

    def run(self):
        print('CameraTask started')
        while True:
            # 打开摄像头
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            last_time = time.time()
            while not cap.isOpened():
                if time.time() - last_time > self.timeout:
                    print('CameraTask: cannot open camera')
                    return
            ret, frame = cap.read()
            if ret:
                # cv2.imshow('frame', frame)
                # cv2.waitKey(1)
                last_time = time.time()
                if self.img_queue.full():
                    self.img_queue.get()
                self.img_queue.put(frame)
            else:
                if time.time() - last_time > self.timeout:
                    print('CameraTask: cannot read frame')
                    return
