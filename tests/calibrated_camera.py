import cv2
import numpy as np

# 创建VideoCapture对象，参数为0表示使用本地摄像头
cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_EXPOSURE, -8)
SIZE = (1280, 720)

# cap.set(cv2.CAP_PROP_EXPOSURE, -8)
cap.set(3, SIZE[0])
cap.set(4, SIZE[1])


def get_x_y(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


camera_matrix = np.load('configs/camera_matrix.npy')
dist_coeffs = np.load('configs/dist_coeffs.npy')

while not cap.isOpened():
    ...

while True:
    #曝光
      #设置曝光值 1.0 - 5000  156.0
    # 从摄像头中读取一帧图像
    ret, frame = cap.read()
    # frame = frame[12: 720, 21: 1280]

    # cv2.circle(frame, (frame.shape[1]//2, frame.shape[0]//2), 2, (255, 0, 0), -1)
    # 显示图像
    cv2.imshow('Origin Camera', frame)
    cv2.setMouseCallback('Origin Camera', get_x_y)
    dst = cv2.undistort(frame, camera_matrix, dist_coeffs)
    cv2.imshow('Calibrated Camera', dst)
    

    # 按下q键退出程序
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
