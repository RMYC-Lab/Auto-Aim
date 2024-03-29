# -*-coding:utf-8-*-
import cv2
import numpy as np
from utils.colors import RED_COLOR, GREEN_COLOR
import json
import math
import time
from structure.marker_target import MarkerTarget as MT
from structure.marker_target import set_center, set_shoot_region, set_full_resolution
from service.uart import UartRobotCtrl
from utils.pid import PIDCtrl
from utils.region import Region
from typing import List

# x_pid = PIDCtrl(0.06, 0.001, 0.01)
# y_pid = PIDCtrl(0.01, 0.01, 0.01)
x_pid = PIDCtrl(130, 10, 1, -25, 25)
y_pid = PIDCtrl(80, 10, 1, -25, 25)


PORT = 'COM3'

# 初始化机器人
robot = UartRobotCtrl(PORT)
times = 3
is_connected = False
shoot_delay = 0.5
max_follow_time = 0.7
max_pitch = 20
min_pitch = -20
while is_connected is False and times > 0:
    is_connected = robot.connect()
    times -= 1

if is_connected is False:
    print('Connect failed')
    raise Exception('Connect failed')

robot.set_robot_mode('free')  # 设置机器人模式为自由模式


SIZE = (1280, 720)
set_full_resolution(*SIZE)
CAMERA_F = 888
MARKER_W = 52
MARKER_H = 28
X_ERROR = 1.5
Y_ERROR = 1.3
# CENTER_POINT = (578, 439)
CENTER_POINT = SIZE[0] // 2, SIZE[1] // 2 + 40
set_center(*CENTER_POINT)
ERROR_DIS = 20
IGNORE_W = 3
IGNORE_H = 10
MIN_W = 5
MIN_H = 5
# 标签点 3D 坐标
# 长 53mm 宽 30mm
# 中心位于其几何中心
MARKER_POINTS = np.array([
    [-MARKER_W / 2, -MARKER_H / 2, 0],
    [MARKER_W / 2, -MARKER_H / 2, 0],
    [MARKER_W / 2, MARKER_H / 2, 0],
    [-MARKER_W / 2, MARKER_H / 2, 0]
], dtype=np.float32)

CORRECT_COLOR = GREEN_COLOR
WRONG_COLOR = RED_COLOR


# BLUE1
# h_min = 87
# h_max = 119
# s_min = 98
# s_max = 228
# v_min = 170
# v_max = 255
# BLUE3
h_min = 70
h_max = 119
s_min = 100
s_max = 228
v_min = 115
v_max = 255
# h_min, s_min, v_min, h_max, s_max, v_max = 0, 0, 0, 179, 255, 255

# 加载摄像头标定数据
camera_matrix = np.load('configs/camera_matrix.npy')
dist_coeffs = np.load('configs/dist_coeffs.npy')


def get_x_y(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


# 打开摄像头
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while not cap.isOpened():
    ...

cap.set(cv2.CAP_PROP_EXPOSURE, -8)
cap.set(3, SIZE[0])
cap.set(4, SIZE[1])


def get_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(param)
        # 获取鼠标点击的位置的颜色值
        # 打印颜色值
        print('HSV:', param[y, x])


last_shoot_time = 0
last_find_time = 0

while True:
    # 读取摄像头的每一帧
    ret, frame = cap.read()
    if not ret:
        continue
    # frame = frame[12: 720, 21: 1280]
    # 校准图像
    frame = cv2.undistort(frame, camera_matrix, dist_coeffs)

    # 显示原始图像
    cv2.imshow('Original Image', frame)

    # 将每一帧从 BGR 转换为 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 创建 HSV 阈值
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # 创建掩码
    mask = cv2.inRange(hsv, lower, upper)

    # 应用掩码到原始 HSV 图像
    filtered = cv2.bitwise_and(hsv, hsv, mask=mask)

    # 将过滤后的 HSV 图像转换为灰度图像
    grey = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

    # 滤波
    # grey = cv2.blur(grey, (3, 3))
    grey = cv2.medianBlur(grey, 3)

    # 显示灰度图像
    cv2.imshow('Grey Image', grey)

    # 闭运算
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    # MORPH_RECT(函数返回矩形卷积核)
    # MORPH_CROSS(函数返回十字形卷积核)
    # MORPH_ELLIPSE(函数返回椭圆形卷积核)
    binary = cv2.morphologyEx(grey, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('Blurred Image', binary)

    # 查找轮廓
    # contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.RETR_EXTERNAL 表示只检测外轮廓
    # cv2.RETR_LIST 检测的轮廓不建立等级关系
    # cv2.RETR_CCOMP 建立两个等级的轮廓, 上一层是边界
    # cv2.RETR_TREE 建立一个等级树结构的轮廓
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓
    # dst = cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

    binary2 = cv2.cvtColor(binary.copy(), cv2.COLOR_GRAY2BGR)

    marker_list: List[MT] = []
    # 遍历每一个轮廓
    for index, each_contour in enumerate(contours):
        if len(each_contour) < 5:
            continue
        # 绘制质心
        mn = cv2.moments(each_contour)
        if mn["m00"] == 0:
            continue
        cX = int(mn["m10"] / mn["m00"])
        cY = int(mn["m01"] / mn["m00"])
        # 获取轮廓的外接矩形
        x, y, w, h = cv2.boundingRect(each_contour)
        # center_x = x + w / 2
        # center_y = y + h / 2
        center_x = cX
        center_y = cY
        if w / h < 1 or w < MIN_W or h < MIN_H:
            # 过滤掉宽高比小于 1 的轮廓 以及宽高小于最小阈值的轮廓
            continue

        # 检查这个轮廓是否在其他轮廓的上方 用于过滤击打标签上方的血量条
        is_above = False
        for other_contour in contours:
            if other_contour is each_contour:
                continue
            other_x, other_y, other_w, other_h = cv2.boundingRect(other_contour)
            other_center_x = other_x + other_w / 2
            other_center_y = other_y + other_h / 2
            other_region = Region(center_x=other_center_x, center_y=other_center_y, w=other_w * IGNORE_W, h=other_h * IGNORE_H,
                                  expand_bottom=False)
            current_ignore_w = IGNORE_W * other_w
            current_ignore_h = IGNORE_H * other_h
            # cv2.rectangle(binary2, (int(other_center_x - current_ignore_w), int(other_center_y - current_ignore_h)), \
            #               (int(other_center_x + current_ignore_w), int(other_center_y)), (0, 0, 255), 1)
            # if other_center_x - current_ignore_w < center_x < other_center_x + current_ignore_w and \
            #         other_center_y - current_ignore_h < center_y < other_center_y:
            if other_region.is_in_region(center_x, center_y):
                is_above = True
                break

        # 如果这个轮廓在其他轮廓的上方，那么忽略这个轮廓
        if is_above:
            continue
        # cv2.rectangle(binary2, (int(center_x - current_ignore_w), int(center_y - current_ignore_h)), \
        #               (int(center_x + current_ignore_w), int(center_y)), (0, 255, 0), 1)

        cv2.imshow(f'Box {index}', binary[y:y + h, x:x + w])
        # 获取最小外接矩形
        min_area = cv2.minAreaRect(each_contour)
        box_point = cv2.boxPoints(min_area)
        box_point = np.int_(box_point)
        # 寻找最小外接矩形的四个顶点
        top_left = box_point[np.argmin(box_point.sum(axis=1))]          # 找到左上角的点
        bottom_right = box_point[np.argmax(box_point.sum(axis=1))]      # 找到右下角的点
        top_right = box_point[np.argmin(np.diff(box_point, axis=1))]    # 找到右上角的点
        bottom_left = box_point[np.argmax(np.diff(box_point, axis=1))]  # 找到左下角的点
        cv2.putText(binary2, str(index) + "TL", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(binary2, str(index) + "TR", top_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(binary2, str(index) + "BL", bottom_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(binary2, str(index) + "BR", bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.drawContours(binary2, [box_point], 0, (0, 255, 0), 2)
        # 绘制最小外接椭圆
        # min_ellipse = cv2.fitEllipse(each_contour)
        # if min_ellipse[0] and min_ellipse[1]:
        #     cv2.ellipse(dst, min_ellipse, (255, 0, 0), 2)
        #     cv2.ellipse(binary2, min_ellipse, (255, 0, 0), 2)
        # 获取误差允许范围
        # current_x_error = X_ERROR * w / 2
        # current_y_error = Y_ERROR * h / 2
        # 绘制误差允许范围
        # cv2.rectangle(binary2, (int(cX - current_x_error), int(cY - current_y_error)),
        #               (int(cX + current_x_error), int(cY + current_y_error)), (0, 0, 255), 1)
        # 判断质心是否在误差允许范围内
        # if CENTER_POINT[0] - current_x_error < cX < CENTER_POINT[0] + current_x_error and \
        #         CENTER_POINT[1] - current_y_error < cY < CENTER_POINT[1] + current_y_error:
        #     cv2.line(binary2, (cX, cY), CENTER_POINT, CORRECT_COLOR, 1)
        # else:
        #     cv2.line(binary2, (cX, cY), CENTER_POINT, WRONG_COLOR, 1)
        # 使用 PNP 求解距离
        # image_points = np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)
        # _, rvec, tvec = cv2.solvePnP(MARKER_POINTS, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
        # flag 参数:
        # SOLVEPNP_ITERATIVE 使用迭代算法寻找最优解
        # SOLVEPNP_P3P 使用 P3P 算法寻找最优解
        # SOLVEPNP_EPNP 使用 EPNP 算法寻找最优解
        # SOLVEPNP_DLS 使用 DLS 算法寻找最优解
        # SOLVEPNP_UPNP 使用 UPNP 算法寻找最优解
        # SOLVEPNP_AP3P 使用 AP3P 算法寻找最优解
        # SOLVEPNP_MAX_COUNT 使用迭代算法寻找最优解时的最大迭代次数
        # distance = math.sqrt(tvec[0]**2 + tvec[1]**2 + tvec[2]**2) / 10
        # rvec_matrix = cv2.Rodrigues(rvec)[0]
        # proj_matrix = np.hstack((rvec_matrix, rvec))
        # eulerAngles = -cv2.decomposeProjectionMatrix(proj_matrix)[6]  # 欧拉角
        # pitch, yaw, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]
        # print(index, "distance:", distance, "pitch:", pitch, "yaw:", yaw, "roll:", roll)
        marker_list.append(MT(x, y, 0, w, h, w*X_ERROR, h*Y_ERROR))
        # cv2.line(dst, (cX, cY), CENTER_POINT, (0, 0, 255), 1)
        # distance = np.sqrt((cX - CENTER_POINT[0]) ** 2 + (cY - CENTER_POINT[1]) ** 2)
        # z = F * MARKER_W / w
        # z_distance = CAMERA_F * MARKER_W / w
        # z_distance2 = CAMERA_F * MARKER_H / h
        # cv2.putText(dst, 'z: {:.2f} {:.2f}'.format(z_distance, z_distance2), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # 绘制质心
        cv2.circle(binary2, (cX, cY), 2, (255, 0, 255), -1)
        cv2.putText(binary2, f"{index} {w}, {h}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.putText(dst, str(index), box_point[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.circle(binary2, (cX, cY), 2, (255, 0, 255), -1)
        # cv2.putText(binary2, str(index), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.putText(binary2, str(index), box_point[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    cv2.putText(binary2, 'Totoal: {}'.format(len(contours)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 显示绘制轮廓后的图像
    # cv2.imshow('Contours', dst)
    # cv2.setMouseCallback('Contours', get_x_y)
    cv2.imshow('Contours2', binary2)

    marker_list.sort(key=lambda target: (target.y + target.h)*(target.w*target.h), reverse=True)
    if len(marker_list) > 0:
        shoot_marker = marker_list[0]
        last_find_time = time.time()
        shoot_region = Region(center_x=CENTER_POINT[0], center_y=CENTER_POINT[1]+40,
                              w=shoot_marker.w * X_ERROR, h=shoot_marker.h * Y_ERROR,
                              expand_bottom=False)
        if shoot_marker.is_shootable(shoot_region) and False:
            if time.time() - last_shoot_time > shoot_delay:
                last_shoot_time = time.time()
                robot.set_blaster_bead(1)
                robot.blaster_fire()
                print('shoot')
        else:
            # 计算PID
            x_pid.set_error(shoot_marker.get_x_error(shoot_region))
            y_pid.set_error(shoot_marker.get_y_error(shoot_region))
            x_output = x_pid.get_output()
            y_output = y_pid.get_output()
            # if not min_pitch <= robot.get_gimbal_attitude()[0] <= max_pitch:
            #     x_output = 0
            robot.gimbal_speed(y_output, x_output)
            print('move')

    if time.time() - last_find_time > max_follow_time:
        # robot.gimbal_speed(0, 0)
        robot.gimbal_recenter()
        print('Lost target')

    # 检查用户是否按下了 'q' 键
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
