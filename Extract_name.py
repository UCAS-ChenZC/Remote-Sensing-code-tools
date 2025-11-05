import os

def save_png_filenames_to_txt(input_folder, output_txt_path):
    # 遍历目录中的所有png文件
    filenames = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith('.png')
    ]

    # 将文件名写入txt文件
    with open(output_txt_path, 'w') as f:
        for name in filenames:
            f.write(name + '\n')
    print(f"Saved {len(filenames)} filenames to {output_txt_path}")

# 示例调用
input_dir = '/media/solid/T9/CZC/511/Plane/label'          # 替换为PNG图像目录
output_txt = '/media/solid/T9/CZC/511/Plane/train.txt'          # 替换为train.txt的保存路径
save_png_filenames_to_txt(input_dir, output_txt)

