# -*- codeing: utf-8 -*- #
"""
# @file             main_docker.py
# @brief            用于找出两个文件夹中的不同图片并存储到新文件夹中
# @note
# @version          V1.00
# @date             2024/8/15 下午3:22
# @author           czc
# @copyright        CIOMP
"""
import os
import shutil

# 设置文件夹路径
folder1_path = '/home/solid/TZ/Datasets/Space_Based_v10/剩余汇总/剩余减小样本'  # 替换为文件夹1的实际路径
folder2_path = '/home/solid/TZ/Datasets/Space_Based_v10/剩余汇总/剩余减小样本txt'  # 替换为文件夹2的实际路径
new_folder_path = '/home/solid/TZ/Datasets/Space_Based_v10/剩余汇总/new_folder'  # 替换为新文件夹的实际路径

# 创建新文件夹（如果尚不存在）
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

# 遍历文件夹2中的所有文件
for filename in os.listdir(folder2_path):
    # 检查文件是否存在于文件夹1中
    if os.path.isfile(os.path.join(folder1_path, filename)):
        # 构建源文件和目标文件的完整路径
        source_file_path = os.path.join(folder1_path, filename)
        target_file_path = os.path.join(new_folder_path, filename)
        
        # 复制文件
        shutil.copy2(source_file_path, target_file_path)
        print(f"文件 {filename} 已复制到 {new_folder_path}")

print("完成文件复制。")
