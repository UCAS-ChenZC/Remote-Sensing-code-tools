'''from PIL import Image
import os

def convert_tif_to_png(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            # 构建输入文件的完整路径
            input_image_path = os.path.join(input_folder, filename)
            
            # 打开图像文件
            with Image.open(input_image_path) as img:
                # 构建输出文件的完整路径
                output_image_path = os.path.join(output_folder, filename[:-4] + '.png')
                
                # 转换并保存图像为PNG格式
                img.save(output_image_path, 'PNG')
                print(f"Converted {filename} to PNG format and saved as {output_image_path}")

    print("All .tif/.tiff images have been converted to .png format.")

# 使用示例
input_folder = '/media/solid/902EAC1C2EABF8FC/datasets/小样本增强1000pix/m_1000pix'  # 替换为你的输入文件夹路径
output_folder = '/media/solid/902EAC1C2EABF8FC/datasets/小样本增强1000pix/m_1000png'  # 替换为你的输出文件夹路径
convert_tif_to_png(input_folder, output_folder)'''
from PIL import Image
import os
import multiprocessing

def convert_image(input_path, output_path):
    # 打开图像文件并转换为PNG格式
    with Image.open(input_path) as img:
        img.save(output_path, 'PNG')

def convert_tif_to_png(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 收集所有tif文件的路径
    tif_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(('.tif', '.tiff'))]
    
    # 定义一个进程池
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # 使用星号解包tif_files列表到每个进程
        pool.starmap(convert_image, [(f, os.path.join(output_folder, os.path.splitext(os.path.basename(f))[0] + '.png')) for f in tif_files])
    
    print("All .tif/.tiff images have been converted to .png format.")

# 使用示例
input_folder = '/media/solid/902EAC1C2EABF8FC/datasets/小样本增强1000pix/m_1000pix'  # 替换为你的输入文件夹路径
output_folder = '/media/solid/902EAC1C2EABF8FC/datasets/小样本增强1000pix/m_1000png'  # 替换为你的输出文件夹路径
convert_tif_to_png(input_folder, output_folder)
