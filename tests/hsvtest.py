# -*-coding:utf-8-*-
import cv2
import numpy as np
from tkinter import Tk, Scale, Button, Frame, StringVar, HORIZONTAL
from tkinter.ttk import Combobox
from tkinter.messagebox import showinfo, showerror, showwarning
from pathlib import Path
import json


SIZE = (1280, 720)
CONFIG_FILE_PATH = Path.cwd() / Path("configs")

print(CONFIG_FILE_PATH.absolute())
if not CONFIG_FILE_PATH.exists():
    CONFIG_FILE_PATH.mkdir()


# 尝试从文件中加载HSV值
def load_value_from_file(file_path: Path):
    if not file_path.exists():
        return None
    with open(file_path, 'r') as f:
        return json.load(f)


def save_value_to_file(file_path: Path, value: dict):
    if not file_path.name.endswith('.json'):
        file_path = file_path.with_suffix('.json')
    with open(file_path, 'w') as f:
        json.dump(value, f)


def on_load_file_btn_click():
    file_name = load_file_str.get()
    if not file_name:
        showwarning('Warning', 'Please select a file first!')
        return
    if not CONFIG_FILE_PATH.joinpath(file_name).exists():
        showerror('Error', 'File not exists!')
        return
    try:
        hsv_values = load_value_from_file(CONFIG_FILE_PATH.joinpath(file_name))
        if not hsv_values:
            showerror('Error', 'File is empty!')
            return
        h_min_scale.set(hsv_values['h_min'])
        h_max_scale.set(hsv_values['h_max'])
        s_min_scale.set(hsv_values['s_min'])
        s_max_scale.set(hsv_values['s_max'])
        v_min_scale.set(hsv_values['v_min'])
        v_max_scale.set(hsv_values['v_max'])
    except KeyError:
        showerror('Error', 'File is invalid!')
        return
    except Exception as e:
        showerror('Error', 'Unknown error: {}'.format(e))
        return
    showinfo('Info', 'Load success!')


def on_save_file_btn_click():
    file_name = load_file_str.get()
    if not file_name:
        showwarning('Warning', 'Please enter a file name first!')
        return
    save_value_to_file(CONFIG_FILE_PATH.joinpath(file_name), {
        'h_min': h_min_scale.get(), 'h_max': h_max_scale.get(),
        's_min': s_min_scale.get(), 's_max': s_max_scale.get(),
        'v_min': v_min_scale.get(), 'v_max': v_max_scale.get()})
    showinfo('Info', 'Save success!')

def reload_config_file_list():
    config_file_list = []
    for each in CONFIG_FILE_PATH.rglob('*.json'):
        config_file_list.append(each.name)
    load_file_cmbox['value'] = tuple(config_file_list)


# 默认值
h_min, s_min, v_min, h_max, s_max, v_max = 0, 0, 0, 179, 255, 255

# 创建滑动条，用于设置 HSV 的最小和最大值
# 创建Tkinter窗口
root = Tk()

# 创建滑动条
TICKINTERVAL = 20
LENGTH = 400
SUM_COLUMNS = 2
file_frame = Frame(root)
file_frame.grid(row=0, column=0, columnspan=SUM_COLUMNS)
load_file_str = StringVar()
load_file_cmbox = Combobox(file_frame, textvariable=load_file_str)
load_file_cmbox['value'] = tuple()
load_file_cmbox.grid(row=0, column=0, padx=10)
load_file_btn = Button(file_frame, text='Load', command=on_load_file_btn_click)
load_file_btn.grid(row=0, column=1, padx=10)
save_file_btn = Button(file_frame, text='Save', command=on_save_file_btn_click)
save_file_btn.grid(row=0, column=2, padx=10)
reload_file_btn = Button(file_frame, text='Reload', command=reload_config_file_list)
reload_file_btn.grid(row=0, column=3, padx=10)
h_min_scale = Scale(root, tickinterval=TICKINTERVAL, length=LENGTH, from_=0, to=179, orient=HORIZONTAL, label='HMin')
h_min_scale.grid(row=1, column=0)
h_max_scale = Scale(root, tickinterval=TICKINTERVAL, length=LENGTH, from_=0, to=179, orient=HORIZONTAL, label='HMax')
h_max_scale.grid(row=1, column=1)
s_min_scale = Scale(root, tickinterval=TICKINTERVAL, length=LENGTH, from_=0, to=255, orient=HORIZONTAL, label='SMin')
s_min_scale.grid(row=2, column=0)
s_max_scale = Scale(root, tickinterval=TICKINTERVAL, length=LENGTH, from_=0, to=255, orient=HORIZONTAL, label='SMax')
s_max_scale.grid(row=2, column=1)
v_min_scale = Scale(root, tickinterval=TICKINTERVAL, length=LENGTH, from_=0, to=255, orient=HORIZONTAL, label='VMin')
v_min_scale.grid(row=3, column=0)
v_max_scale = Scale(root, tickinterval=TICKINTERVAL, length=LENGTH, from_=0, to=255, orient=HORIZONTAL, label='VMax')
v_max_scale.grid(row=3, column=1)

# 设置滑动条的默认值
h_min_scale.set(h_min)
h_max_scale.set(h_max)
s_min_scale.set(s_min)
s_max_scale.set(s_max)
v_min_scale.set(v_min)
v_max_scale.set(v_max)

reload_config_file_list()

# 创建滑动条，用于调整曝光
# cv2.createTrackbar('Exposure', 'HSV Filter', -10, 10, lambda x: None)

# 打开摄像头
cap = cv2.VideoCapture(0)

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


while True:
    root.update()
    # 获取滑动条的当前位置
    # exposure = cv2.getTrackbarPos('Exposure', 'HSV Filter')

    # 设置曝光
    # cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

    # 读取摄像头的每一帧
    _, frame = cap.read()

    # 显示原始图像
    cv2.imshow('Original Image', frame)

    # 将每一帧从 BGR 转换为 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 显示 HSV 图像
    # cv2.imshow('HSV Image', hsv)

    # 分解 HSV 图像为三个通道
    h, s, v = cv2.split(hsv)

    # 分别显示 H，S，V 通道
    # cv2.imshow('H Channel', h)
    # cv2.imshow('S Channel', s)
    # cv2.imshow('V Channel', v)

    # 获取滑动条的当前位置    
    h_min = h_min_scale.get()
    s_min = s_min_scale.get()
    v_min = v_min_scale.get()
    h_max = h_max_scale.get()
    s_max = s_max_scale.get()
    v_max = v_max_scale.get()

    # 添加鼠标点击事件 (用于获取鼠标点击的位置的颜色值)
    # cv2.setMouseCallback('HSV Image', get_color, param=hsv)
    # cv2.setMouseCallback('H Channel', get_color, param=h)
    # cv2.setMouseCallback('S Channel', get_color, param=s)
    # cv2.setMouseCallback('V Channel', get_color, param=v)

    # 创建 HSV 阈值
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # 创建掩码
    mask = cv2.inRange(hsv, lower, upper)

    # 应用掩码到原始 HSV 图像
    filtered = cv2.bitwise_and(hsv, hsv, mask=mask)

    # 显示过滤后的 HSV 图像
    # cv2.imshow('Filtered HSV Image', filtered)

    # 拼接图像并显示
    # hsv_imgs = cv2.vconcat([h, s, v])
    # cv2.imshow('HSV Images', hsv_imgs)
    # cv2.setMouseCallback('HSV Images', get_color, param=hsv_imgs)

    # 将过滤后的 HSV 图像转换为灰度图像
    grey = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

    # 滤波
    # grey = cv2.blur(grey, (3, 3))
    grey = cv2.medianBlur(grey, 3)

    # 显示灰度图像
    cv2.imshow('Grey Image', grey)
    
    # 将灰度图像转换为二值图像 (二值化)
    # ret, binary = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)
    
    # 显示二值图像
    # cv2.imshow('Binary Image', binary)

    # 腐蚀
    # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    # grey = cv2.erode(grey, kernel1, iterations = 1)

    # 闭运算
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(grey, cv2.MORPH_CLOSE, kernel)
    # MORPH_RECT(函数返回矩形卷积核)
    # MORPH_CROSS(函数返回十字形卷积核)
    # MORPH_ELLIPSE(函数返回椭圆形卷积核)

    cv2.imshow('Blurred Image', binary)

    # 查找轮廓
    # contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.RETR_EXTERNAL 表示只检测外轮廓
    # cv2.RETR_LIST 检测的轮廓不建立等级关系
    # cv2.RETR_CCOMP 建立两个等级的轮廓,上一层是边界
    # cv2.RETR_TREE 建立一个等级树结构的轮廓
    #
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓
    dst = cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

    binary2 = cv2.cvtColor(binary.copy(), cv2.COLOR_GRAY2BGR)

    for index, each_contour in enumerate(contours):
        if len(each_contour) < 5:
            continue
        # 绘制最小外接矩形
        min_area = cv2.minAreaRect(each_contour)
        box_point = cv2.boxPoints(min_area)
        box_point = np.int_(box_point)
        # 找到左上角的点
        top_left = box_point[np.argmin(box_point.sum(axis=1))]
        # 找到右下角的点
        bottom_right = box_point[np.argmax(box_point.sum(axis=1))]
        # 找到右上角的点
        top_right = box_point[np.argmin(np.diff(box_point, axis=1))]
        # 找到左下角的点
        bottom_left = box_point[np.argmax(np.diff(box_point, axis=1))]
        cv2.putText(binary2, str(index) + "TL", top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(binary2, str(index) + "TR", top_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(binary2, str(index) + "BL", bottom_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(binary2, str(index) + "BR", bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.drawContours(dst, [box_point], 0, (0, 255, 0), 2)
        cv2.drawContours(binary2, [box_point], 0, (0, 255, 0), 2)
        # cv2.putText(binary2, str(index) + "0", box_point[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.putText(binary2, str(index) + "1", box_point[1], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.putText(binary2, str(index) + "2", box_point[2], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.putText(binary2, str(index) + "3", box_point[3], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # 绘制最小外接椭圆
        # min_ellipse = cv2.fitEllipse(each_contour)
        # cv2.ellipse(dst, min_ellipse, (255, 0, 0), 2)
        # cv2.ellipse(binary2, min_ellipse, (255, 0, 0), 2)
        # Hu矩
        # compute the center of the contour
        mn = cv2.moments(each_contour)
        if mn["m00"] == 0:
            continue
        cX = int(mn["m10"] / mn["m00"])
        cY = int(mn["m01"] / mn["m00"])
        humn = cv2.HuMoments(mn)
        cv2.circle(dst, (cX, cY), 2, (255, 0, 255), -1)
        cv2.putText(dst, str(index), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.putText(dst, str(index), box_point[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.circle(binary2, (cX, cY), 2, (255, 0, 255), -1)
        cv2.putText(binary2, str(index), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        # cv2.putText(binary2, str(index), box_point[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        print(index, humn)
        # cv2.putText(frame, "Hu Moments: {}".format(humn), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(binary2, 'Totoal: {}'.format(len(contours)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    # 显示绘制轮廓后的图像
    cv2.imshow('Contours', dst)
    cv2.imshow('Contours2', binary2)

    # 检查用户是否按下了 'q' 键
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
