'''
# -*- codeing: utf-8 -*- #
"""
# @file            del_1.py
# @brief            # 去除文件名最后的指定字符
# @note
# @version          V1.00
# @date             2024/8/15 下午3:22
# @author           czc
# @copyright        CIOMP
"""
import os

def remove_last_two_characters(file_path, characters='_1'):
    # 去除文件名最后的指定字符
    file_name = os.path.basename(file_path)
    file_name_without_characters = os.path.splitext(file_name)[0].rstrip(characters)
    new_file_name = f"{file_name_without_characters}{os.path.splitext(file_name)[1]}"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    return new_file_path

def process_folder(input_folder):
    # 遍历文件夹中的所有文件
    for file_path in os.listdir(input_folder):
        full_file_path = os.path.join(input_folder, file_path)
        if os.path.isfile(full_file_path):
            new_file_path = remove_last_two_characters(full_file_path)
            # 重命名文件
            os.rename(full_file_path, new_file_path)
            print(f"Renamed '{full_file_path}' to '{new_file_path}'")

# 使用示例
input_folder = '/media/solid/902EAC1C2EABF8FC/datasets/TenCar/validation/gt'  # 替换为你的文件夹路径
process_folder(input_folder)'''

'''import os

def remove_first_character(filename, character='P'):
    # 检查文件名是否以指定字符开头
    if filename.startswith(character):
        # 去除文件名第1位的指定字符
        new_filename = filename[1:]
    else:
        new_filename = filename
    return new_filename

def process_files_in_folder(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 确保是文件而不是文件夹
        if os.path.isfile(file_path):
            new_filename = remove_first_character(filename)
            new_file_path = os.path.join(folder_path, new_filename)
            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f"Renamed '{file_path}' to '{new_file_path}'")

# 使用示例
folder_path = '/output_path124pt'  # 替换为你的文件夹路径
process_files_in_folder(folder_path)'''

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
images_folder_path = '/home/solid/LYD/images/回填图片'  # 数量多的  文件夹路径1
tags_folder_path = '/home/solid/LYD/111/images'  # 数量少的 标签文件夹路径2
output_path = '/home/solid/LYD/222'  # 数量相差的文件作为输出的  文件夹路径3

keep_images_without_matching_xml_tags(images_folder_path, tags_folder_path, output_path)
