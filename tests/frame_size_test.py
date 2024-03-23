import cv2

# 创建一个摄像头对象
cap = cv2.VideoCapture(0)

while not cap.isOpened():
    ...

# 遍历所有可能的分辨率
for width in range(1920, 0, -1):
    for height in range(1080, 0, -1):
        # 尝试设置摄像头的分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # 检查设置是否成功
        if cap.get(cv2.CAP_PROP_FRAME_WIDTH) == width and cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == height:
            # 如果设置成功，那么拍照并保存图片
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(f'{width}x{height}.jpg', frame)

# 释放摄像头
cap.release()
