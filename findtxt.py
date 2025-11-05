


import os
import shutil

def copy_files_with_matching_names(source_folder, target_folder, keywords_file):
    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # 读取包含关键词的文件
    with open(keywords_file, 'r') as f:
        keywords = [line.strip() for line in f if line.strip()]

    # 遍历源文件夹中的所有文件
    for file_name in os.listdir(source_folder):
        # 检查文件扩展名是否为.txt
        if file_name.endswith('.txt'):
            file_path = os.path.join(source_folder, file_name)
            # 检查文件名（不包含扩展名）是否在关键词列表中
            if os.path.splitext(file_name)[0] in keywords:
                # 构建目标文件的完整路径
                target_file_path = os.path.join(target_folder, file_name)
                # 复制文件
                shutil.copy(file_path, target_file_path)
                print(f"文件 '{file_name}' 已复制到 '{target_folder}'")

# 使用示例
source_directory_path = '/home/solid/TZ/Datasets/Space_Based_v10/剩余txt'   # 指定源文件夹路径
target_directory_path = '/home/solid/TZ/Datasets/Space_Based_v10/小样本txt2' # 指定目标文件夹路径
keywords_file_path ='/home/solid/my_tools/2.txt'        # 指定包含关键词的txt文件路径

# 调用函数
copy_files_with_matching_names(source_directory_path, target_directory_path, keywords_file_path)
