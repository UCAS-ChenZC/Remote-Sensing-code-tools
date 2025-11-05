import os
import xml.etree.ElementTree as ET

def adjust_xml(xml_file):
    # 解析XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取 <size> 标签并检查宽高
    size = root.find('size')
    if size is not None:
        width = size.find('width')
        height = size.find('height')
        if width is not None and height is not None:
            # 判断宽高是否为 1080x1920，如果是则交换
            if width.text == '1080' and height.text == '1920':
                # 交换宽高
                width.text, height.text = height.text, width.text
                print(f"Modified: {xml_file}")

    # 保存修改后的XML文件
    tree.write(xml_file)

def batch_adjust_xml_in_folder(folder_path):
    # 遍历文件夹中的所有XML文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_file = os.path.join(folder_path, filename)
            adjust_xml(xml_file)

# 设置文件夹路径
folder_path = '/home/solid/CD/ciomp/吉林农大-20241118/output/3023已筛选'  # 修改为你文件夹的路径

# 批量修改文件夹中的XML文件
batch_adjust_xml_in_folder(folder_path)

