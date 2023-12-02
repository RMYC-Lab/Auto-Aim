import cv2

camera = cv2.VideoCapture(1)

SIZE = (1280, 720)

# camera.set(cv2.CAP_PROP_EXPOSURE, -4)
camera.set(3, SIZE[0])
camera.set(4, SIZE[1])

# 棋盘格每行每列角点个数
BOARDSIZE = (6, 9)


while not camera.isOpened():
    ...

i = 0

while True:
    _, frame = camera.read()
    cv2.imshow('Frame', frame)

    # frame2 = frame.copy()

    # img_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # # 检测角点
    # found_success, img_corner_points = cv2.findChessboardCorners(img_gray, BOARDSIZE, None)

    # # 显示角点
    # if found_success:
    #     # 迭代终止条件
    #     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #     # 进一步提取亚像素角点
    #     cv2.cornerSubPix(img_gray, img_corner_points, (11, 11), (-1, -1), criteria)

    #     # 绘制角点
    #     cv2.drawChessboardCorners(frame2, BOARDSIZE, img_corner_points, found_success)
    # cv2.imshow("Frame2", frame2)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("Q"): # 按ESC键退出
        break
    elif key & 0xFF == ord(" "):
        cv2.imwrite(r"images\\"+str(i)+'.png', frame, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        print("Saved image", i)
        i += 1

camera.release()
cv2.destroyAllWindows()
