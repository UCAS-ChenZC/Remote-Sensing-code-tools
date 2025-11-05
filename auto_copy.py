import os
import shutil
from concurrent.futures import ThreadPoolExecutor

def copy_image(input_path, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 构建输出文件的完整路径
    output_path = os.path.join(output_folder, os.path.basename(input_path))
    
    # 复制文件
    shutil.copy(input_path, output_path)

def copy_images(input_folder, output_folder):
    # 获取所有图片文件的路径
    images = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    # 使用线程池来并行复制文件
    with ThreadPoolExecutor(max_workers=10) as executor:  # 你可以根据你的CPU核心数调整线程数
        executor.map(lambda x: copy_image(x, output_folder), images)
    
    print("All images have been copied to the output folder.")

# 使用示例
input_folder = '/media/solid/902EAC1C2EABF8FC/datasets/小样本增强1000pix/m_1000png'  # 替换为你的输入文件夹路径
output_folder = '/media/solid/LiuYD/m_1000png'  # 替换为你的输出文件夹路径
copy_images(input_folder, output_folder)
