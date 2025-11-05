import os
import cv2
import numpy as np

# 创建存放图像的文件夹
save_dir = "/home/solid/CD/222"
os.makedirs(save_dir, exist_ok=True)

# 图像尺寸
H, W = 256, 256

# 图像1：包含一个小区域（10x10），应被框出
img1 = np.zeros((H, W), dtype=np.uint8)
cv2.rectangle(img1, (50, 50), (60, 60), 255, -1)
cv2.imwrite(os.path.join(save_dir, "change_small_1.png"), img1)

# 图像2：两个小区域（各不超过15x15），应被框出
img2 = np.zeros((H, W), dtype=np.uint8)
cv2.rectangle(img2, (100, 100), (113, 113), 255, -1) # 13x13
cv2.rectangle(img2, (150, 50), (160, 60), 255, -1) # 10x10
cv2.imwrite(os.path.join(save_dir, "change_small_2.png"), img2)

# 图像3：包含一个大区域（30x30），不应被框出
img3 = np.zeros((H, W), dtype=np.uint8)
cv2.rectangle(img3, (60, 60), (90, 90), 255, -1)
cv2.imwrite(os.path.join(save_dir, "change_large_1.png"), img3)

# 图像4：两个大区域，均不应被框出
img4 = np.zeros((H, W), dtype=np.uint8)
cv2.rectangle(img4, (30, 30), (60, 60), 255, -1)
cv2.rectangle(img4, (120, 120), (140, 160), 255, -1)
cv2.imwrite(os.path.join(save_dir, "change_large_2.png"), img4)

print("测试图像已生成完毕！目录：111")
