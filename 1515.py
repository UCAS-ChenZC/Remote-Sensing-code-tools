import cv2
import numpy as np
import os

# 设置输入和输出路径
input_dir = "/home/solid/CD/222" # 输入图像所在文件夹
output_dir = "/home/solid/CD/333" # 输出图像保存文件夹
os.makedirs(output_dir, exist_ok=True)

MAX_SIZE = 15
MAX_AREA = MAX_SIZE * MAX_SIZE

# 遍历输入文件夹中的所有图像
for filename in os.listdir(input_dir):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif')):
        continue

    filepath = os.path.join(input_dir, filename)
    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"跳过无法读取的图像：{filename}")
        continue

    # 提取轮廓
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    found = False

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)

        if w <= MAX_SIZE and h <= MAX_SIZE and area <= MAX_AREA:
            # 画固定 15x15 的红色框
            cv2.rectangle(output_img, (x, y), (x + 15, y + 15), (0, 0, 255), 1)
            found = True

    if found:
        # 只保存符合条件的图像
        out_path = os.path.join(output_dir, filename)
        cv2.imwrite(out_path, output_img)
        print(f"✔ 已输出符合条件图像：{filename}")

print("✅ 筛选输出完成，只输出包含小变化区域的图像。")


