# -*- codeing: utf-8 -*- #
"""
# @file             main_docker.py
# @brief            用于找出两个文件夹中不同名的图片并存储到新文件夹中
# @note
# @version          V1.00
# @date             2024/8/15 下午3:22
# @author           czc
# @copyright        CIOMP
"""
import os
import shutil

def keep_images_without_matching_xml_tags(images_folder, tags_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 获取所有.xml文件的文件名（不含扩展名）
    xml_tags = {os.path.splitext(f)[0] for f in os.listdir(tags_folder) if f.endswith('.tif')}
    
    # 遍历图片文件夹中的所有.tif文件
    for image_name in os.listdir(images_folder):
        if image_name.endswith('.tif'):
            # 获取不带扩展名的图片文件名
            image_stem = os.path.splitext(image_name)[0]
            # 检查当前图片是否与.xml文件标签同名
            if image_stem not in xml_tags:
                # 图片与.xml标签不匹配，复制到输出文件夹
                original_image_path = os.path.join(images_folder, image_name)
                output_image_path = os.path.join(output_folder, image_name)
                shutil.copy(original_image_path, output_image_path)
                print(f"Copied '{image_name}' to '{output_folder}' because it does not match any XML tags.")

# 使用示例
images_folder_path = ' '  # 数量多的  文件夹路径1
tags_folder_path = ' '  # 数量少的 标签文件夹路径2
output_path = ' '  # 数量相差的文件作为输出的  文件夹路径3

keep_images_without_matching_xml_tags(images_folder_path, tags_folder_path, output_path)
