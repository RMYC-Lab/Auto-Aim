import cv2
import numpy as np
import glob

# 棋盘格每行每列角点个数
BOARDSIZE = (6, 9)
# 棋盘格每个格子的物理尺寸 单位: mm
DISTANCE = 21

# 保存棋盘格上角点的三维坐标
objpoints_img = []

# 三维世界坐标
obj_world_pts = np.zeros((np.prod(BOARDSIZE), 3), np.float32)
obj_world_pts[:, :2] = np.indices(BOARDSIZE).T.reshape(-1, 2) * DISTANCE

# 保存所有角点
images_points = []

# 待处理图路径
image_path = "images/*.png"

# 读取指定文件夹下图像
images_path = glob.glob(image_path)

for path in images_path:
    image = cv2.imread(path)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 检测角点
    found_success, img_corner_points = cv2.findChessboardCorners(img_gray, BOARDSIZE, None)

    # 显示角点
    if found_success:
        # 迭代终止条件
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # 进一步提取亚像素角点
        cv2.cornerSubPix(img_gray, img_corner_points, (11, 11), (-1, -1), criteria)

        # 绘制角点
        cv2.drawChessboardCorners(image, BOARDSIZE, img_corner_points, found_success)

        objpoints_img.append(obj_world_pts)
        images_points.append(img_corner_points)

    # 显示棋盘格角点
    cv2.imshow('image', image)
    cv2.waitKey(200)

# 计算内参和畸变系数等
_, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints_img, images_points, img_gray.shape[::-1], None, None)

print("camera_matrix:")
print(camera_matrix)

print("*****************************")
print("dist_coeffs:")
print(dist_coeffs)

print("*****************************")
print("Rotation vector:")
print(rvecs)

print("*****************************")
print("Translation vector:")
print(tvecs)

# 畸变图像校准
dst = cv2.undistort(image, camera_matrix, dist_coeffs)

# 保存校准结果
np.save("configs/camera_matrix.npy", camera_matrix, allow_pickle=False)
np.save("configs/dist_coeffs.npy", dist_coeffs, allow_pickle=False)

cv2.imwrite("images/result.jpg", dst)

cv2.destroyAllWindows()  # 销毁显示窗口
