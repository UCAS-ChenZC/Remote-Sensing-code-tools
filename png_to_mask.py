import os
from PIL import Image
import numpy as np

def convert_png_to_binary_mask(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)  # 保留原文件名

            # 打开图像并转换为灰度
            img = Image.open(input_path).convert('L')  # 转为灰度图
            img_array = np.array(img)

            # 二值化处理
            binary_array = np.where(img_array > 0, 255, 0).astype(np.uint8)

            # 保存为PNG格式
            binary_img = Image.fromarray(binary_array)
            binary_img.save(output_path)
            print(f"Saved binary mask: {output_path}")

# 示例调用
input_dir = '/home/solid/桌面/820To_Yao/处理后/mask'      # 替换为你的png图像目录
output_dir = '/home/solid/桌面/820To_Yao/处理后/label'    # 替换为输出掩膜的目录
convert_png_to_binary_mask(input_dir, output_dir)

