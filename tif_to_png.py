import os
from PIL import Image

# 将.tif图像转换为.png格式

def convert_tif_to_png(input_folder, output_folder):
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
            # 构造输入文件和输出文件路径
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.png'
            output_path = os.path.join(output_folder, output_filename)

            # 打开.tif图像并保存为.png格式
            with Image.open(input_path) as img:
                img.convert('RGB').save(output_path, 'PNG')
                print(f"Converted: {input_path} -> {output_path}")

# 示例调用
input_dir = ''     # 替换为你的.tif图像所在目录
output_dir = '' # 替换为你希望保存png图像的目录
convert_tif_to_png(input_dir, output_dir)

