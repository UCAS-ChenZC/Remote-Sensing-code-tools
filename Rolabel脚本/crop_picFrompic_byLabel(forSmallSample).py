import cv2

# 读取xml
import os
import shutil, os
import xml.etree.ElementTree as ET
import sys

sys.setrecursionlimit(3000)

# 筛选
path = "D:\Remote_Sensor_dataset\\validation\labelXmls_littleshot"  # 文件夹目录
image_path = "D:\Remote_Sensor_dataset\\validation\images_littleshot"  # 图片目录
files = os.listdir(path)  # 得到文件夹下的所有文件名称
s = []


def deep_copy_element(element):
    # 创建一个具有相同标签和属性的新元素
    new_element = ET.Element(element.tag, element.attrib)
    # 复制文本内容
    new_element.text = element.text
    # 递归复制子节点
    for child in element:
        new_element.append(deep_copy_element(child))
    return new_element


for file in files:

    # 图片路径
    image_file = image_path + "\\" + file[:-4] + '.tif'
    # 读取原始图像
    image = cv2.imread(image_file)

    tree = ET.parse(path + "\\" + file)

    root = tree.getroot()

    pic_count = 0

    object_list = []
    # 创建新的xml
    # root = ET.Element('data')

    for child in root:
        if child.tag == 'objects':
            # object
            for each in child:

                for x in each:
                    if x.tag == 'possibleresult':

                        x1, y1 = 0, 0
                        x2, y2 = 0, 0
                        x3, y3 = 0, 0
                        x4, y4 = 0, 0

                        class_flag = ''
                        for z in x:
                            flag = False
                            if z.text == 'Bus':
                                flag = True
                                class_flag = 'Bus'
                                pic_count += 1
                                print('Bus')
                            if z.text == 'Trailer':
                                flag = True
                                class_flag = 'Trailer'
                                pic_count += 1
                                print('Trailer')
                            if z.text == 'Tractor':
                                flag = True
                                class_flag = 'Tractor'
                                pic_count += 1
                                print('Tractor')
                            if z.text == 'Excavator':
                                flag = True
                                class_flag = 'Excavator'
                                pic_count += 1
                                print('Excavator')
                            if z.text == 'Truck Tractor':
                                flag = True
                                class_flag = 'Truck Tractor'
                                pic_count += 1
                                print('Truck Tractor')
                            if flag:
                                childcopy = each

                                copied_node = deep_copy_element(childcopy)

                                for points in each:
                                    if points.tag == 'points':
                                        for index, each_point in enumerate(points):
                                            if index == 0:
                                                x1, y1 = each_point.text.split(',')
                                            if index == 1:
                                                x2, y2 = each_point.text.split(',')
                                            if index == 2:
                                                x3, y3 = each_point.text.split(',')
                                            if index == 3:
                                                x4, y4 = each_point.text.split(',')

                                # anchor box
                                print(x1, y1, x2, y2, x3, y3, x4, y4)
                                x1, x2, x3, x4, y1, y2, y3, y4 = int(float(x1)), int(float(x2)), int(float(x3)), int(
                                    float(x4)), int(float(y1)), int(float(y2)), int(float(y3)), int(float(y4))
                                middle_x = int((x1 + x2 + x3 + x4) / 4)
                                middle_y = int((y1 + y2 + y3 + y4) / 4)

                                # 200*200(裁剪后图像大小)
                                # 假设你已经获得了目标框的坐标 (x, y, w, h)
                                x, y, w, h = (middle_x - 100) if (middle_x - 100) >= 0 else 0, (middle_y - 100) if (
                                                                                                                               middle_y - 100) >= 0 else 0, 200, 200
                                # image:w,h
                                a, b, c, d = y, (y + h) if (y + h) <= image.shape[0] else image.shape[0], x, (
                                            x + w) if (x + w) <= image.shape[1] else image.shape[1]
                                # 根据目标框坐标裁剪图像
                                cropped_image = image[a:b, c:d]

                                # 保存裁剪后的图像
                                cv2.imwrite("D:\Remote_Sensor_dataset\\validation\crop\\v_" + file[
                                                                                               :-4] + '_' + class_flag + '_' + str(
                                    pic_count) + '.tif', cropped_image)

                                newroot = root
                                # 生成xml
                                for child in list(newroot.find('objects')):
                                    newroot.find('objects').remove(child)

                                print(x1, y1, x2, y2, x3, y3, x4, y4)

                                for every in copied_node.find('points'):
                                    x_, y_ = every.text.split(',')
                                    x_, y_ = float(x_), float(y_)
                                    x_ = "{:.6f}".format(x_ - x)
                                    y_ = "{:.6f}".format(y_ - y)
                                    every.text = str(x_) + ',' + str(y_)

                                print(ET.tostring(copied_node, encoding='unicode'))

                                # 将复制的节点添加到目标节点下
                                newroot.find('objects').append(copied_node)
                                print(ET.tostring(newroot, encoding='unicode'))
                                # copy_element(childcopy, newroot.find('objects'))

                                tree = ET.ElementTree(newroot)
                                xmlname = "D:\Remote_Sensor_dataset\\validation\croplabel\\v_" + file[
                                                                                                    :-4] + '_' + class_flag + '_' + str(
                                    pic_count) + '.xml'
                                tree.write(xmlname, encoding='utf-8', xml_declaration=True)
                                print('save success')
