# -*-coding:utf-8-*-
import cv2
import numpy as np

# 创建一个空窗口用于放置滑动条
# cv2.namedWindow('BGR Filter')

# 创建滑动条，用于设置 BGR 的最小和最大值
# cv2.createTrackbar('HMin', 'BGR Filter', 0, 179, lambda x: None)
# cv2.createTrackbar('SMin', 'BGR Filter', 0, 255, lambda x: None)
# cv2.createTrackbar('VMin', 'BGR Filter', 0, 255, lambda x: None)
# cv2.createTrackbar('HMax', 'BGR Filter', 179, 179, lambda x: None)
# cv2.createTrackbar('SMax', 'BGR Filter', 255, 255, lambda x: None)
# cv2.createTrackbar('VMax', 'BGR Filter', 255, 255, lambda x: None)


# 创建滑动条，用于调整曝光
# cv2.createTrackbar('Exposure', 'BGR Filter', -10, 10, lambda x: None)

# 打开摄像头
cap = cv2.VideoCapture(0)

while not cap.isOpened():
    ...

while True:
    # 获取滑动条的当前位置
    # exposure = cv2.getTrackbarPos('Exposure', 'BGR Filter')

    # 设置曝光
    # cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

    # 读取摄像头的每一帧
    _, frame = cap.read()

    # 显示原始图像
    cv2.imshow('Original Image', frame)

    # 分解 BGR 图像为三个通道
    b, g, r = cv2.split(frame)

    # 分别显示 B G R 通道
    cv2.imshow('B Channel', b)
    cv2.imshow('G Channel', g)
    cv2.imshow('R Channel', r)
    # cv2.imshow('R2 Channel', np.clip(r, 200, 230))
    ret, r2=cv2.threshold(r, 230, 255, cv2.THRESH_BINARY);
    cv2.imshow('R2 Channel', r2)

    # 获取滑动条的当前位置
    # h_min = cv2.getTrackbarPos('HMin', 'BGR Filter')
    # s_min = cv2.getTrackbarPos('SMin', 'BGR Filter')
    # v_min = cv2.getTrackbarPos('VMin', 'BGR Filter')
    # h_max = cv2.getTrackbarPos('HMax', 'BGR Filter')
    # s_max = cv2.getTrackbarPos('SMax', 'BGR Filter')
    # v_max = cv2.getTrackbarPos('VMax', 'BGR Filter')

    # 创建 BGR 阈值
    # lower = np.array([h_min, s_min, v_min])
    # upper = np.array([h_max, s_max, v_max])

    # 创建掩码
    # mask = cv2.inRange(BGR, lower, upper)

    # 应用掩码到原始 BGR 图像
    # filtered = cv2.bitwise_and(BGR, BGR, mask=mask)

    # 显示过滤后的 BGR 图像
    # cv2.imshow('Filtered BGR Image', filtered)

    # 检查用户是否按下了 'q' 键
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
