import os
import xml.etree.ElementTree as ET
from PIL import Image
from xml.dom import minidom

def txt_to_xml(txt_file_path, image_file_path, xml_file_path):
    # 打开图像文件以获取尺寸
    with Image.open(image_file_path) as img:
        image_width, image_height = img.size

    # 创建XML根元素
    annotation = ET.Element("annotation")
    # 添加source元素
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "filename").text = os.path.basename(image_file_path)
    ET.SubElement(source, "origin").text = "Optical"
    # 添加research元素
    # ... 添加research元素的代码 ...
    # 添加size元素
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(image_width)
    ET.SubElement(size, "height").text = str(image_height)
    ET.SubElement(size, "depth").text = "3"  # 根据图像的实际通道数修改

    objects = ET.SubElement(annotation, "objects")

    # 读取txt文件并创建object元素
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 9:  # 确保有足够的数据
                print(parts)
                x1, y1, x2, y2, x3, y3, x4, y4, class_name, _ = parts
                object_elem = ET.SubElement(objects, "object")
                ET.SubElement(object_elem, "coordinate").text = "pixel"
                ET.SubElement(object_elem, "type").text = "rectangle"
                ET.SubElement(object_elem, "description").text = "None"
                possibleresult = ET.SubElement(object_elem, "possibleresult")
                ET.SubElement(possibleresult, "name").text = class_name

                points = ET.SubElement(object_elem, "points")
                ET.SubElement(points, "point").text = f"{x1},{y1}"
                ET.SubElement(points, "point").text = f"{x2},{y2}"
                ET.SubElement(points, "point").text = f"{x3},{y3}"
                ET.SubElement(points, "point").text = f"{x4},{y4}"

    # 使用minidom美化XML字符串
    xmlstr = ET.tostring(annotation, 'utf-8')
    pretty_xml = minidom.parseString(xmlstr).toprettyxml(indent="\t")

    # 写入XML文件
    with open(xml_file_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

# 图像文件夹路径
image_folder_path = '/media/solid/902EAC1C2EABF8FC/datasets/Space_Based_v9/val/images'
# txt标签文件夹路径
txt_folder_path = '/media/solid/902EAC1C2EABF8FC/datasets/Space_Based_v9/val/txt_gt'
# XML标注输出文件夹路径
xml_output_path = '/media/solid/902EAC1C2EABF8FC/datasets/Space_Based_v9/val/test_val'

# 确保输出目录存在
if not os.path.exists(xml_output_path):
    os.makedirs(xml_output_path)

# 遍历txt标签文件夹中的所有txt文件
for txt_file in os.listdir(txt_folder_path):
    if txt_file.endswith('.txt'):
        txt_file_path = os.path.join(txt_folder_path, txt_file)
        # 从txt文件名中提取图像文件名，并构建图像文件的路径
        image_file_name = os.path.splitext(txt_file)[0] + '.tif'  # 根据图像文件的实际扩展名调整
        image_file_path = os.path.join(image_folder_path, image_file_name)

        # 确保图像文件存在
        if not os.path.isfile(image_file_path):
            print(f"图像文件 {image_file_path} 不存在，跳过该标签文件。")
            continue

        # 构建XML文件的完整路径
        xml_file_name = os.path.splitext(txt_file)[0] + '.xml'
        xml_file_path = os.path.join(xml_output_path, xml_file_name)

        # 执行转换
        txt_to_xml(txt_file_path, image_file_path, xml_file_path)

print("转换完成。")

'''
import os
import os.path
import numpy as np
import cv2
import matplotlib.pyplot as plt

train_list = os.listdir("/home/solid/可视化汇总1/回填第二波/txt/")
base_path = "/home/solid/可视化汇总1/回填第二波/txt/"

total_dict = []

for file in train_list:
    with open(base_path + file) as f:
        s = f.readlines()
        for si in s:
            bbox_info = si.split()
            if bbox_info[8] in total_dict:
                continue
            else:
                total_dict.append(bbox_info[8])
print(total_dict)
print(len(total_dict))'''

