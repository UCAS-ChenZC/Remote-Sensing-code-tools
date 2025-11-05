from xml.etree import ElementTree as ET
import os
import math
import numpy as np

def rotate(angle, x, y):
    """
    基于原点的弧度旋转
    :param angle:   弧度
    :param x:       x
    :param y:       y
    :return:
    """
    rotatex = math.cos(angle) * x - math.sin(angle) * y
    rotatey = math.cos(angle) * y + math.sin(angle) * x
    return rotatex, rotatey


def xy_rorate(theta, x, y, centerx, centery):
    """
    针对中心点进行旋转
    :param theta:
    :param x:
    :param y:
    :param centerx:
    :param centery:
    :return:
    """
    r_x, r_y = rotate(theta, x - centerx, y - centery)
    return centerx + r_x, centery + r_y


def rec_rotate(x, y, width, height, theta):
    """
    传入矩形的x,y和宽度高度，弧度，转成QUAD格式
    :param x:
    :param y:
    :param width:
    :param height:
    :param theta:
    :return:
    """
    centerx = x + width / 2
    centery = y + height / 2

    x1, y1 = xy_rorate(theta, x, y, centerx, centery)
    x2, y2 = xy_rorate(theta, x + width, y, centerx, centery)
    x3, y3 = xy_rorate(theta, x, y + height, centerx, centery)
    x4, y4 = xy_rorate(theta, x + width, y + height, centerx, centery)

    return x1, y1, x2, y2, x4, y4, x3, y3

convert_options = {}

def convert_XML_to_DOTA(filename):
    mydoc = ET.parse(filename)
    root = mydoc.getroot()

    # objects = root.find('objects')
    items = root.findall('object')
    output_file = os.path.splitext(os.path.split(filename)[-1])[0] + '.txt'
    with open(f'/home/solid/CD/ciomp/SAR/txt/{output_file}', 'w') as f:   # txt
        ann_list = []
        for item in items:
            label = item.find('name').text
            if item.find('type').text == 'bndbox':
                xmin, ymin, xmax, ymax= item.find('bndbox/xmin').text, item.find('bndbox/ymin').text, item.find(
                    'bndbox/xmax').text, item.find('bndbox/ymax').text
                xmin, ymin, xmax, ymax = int(float(xmin)), int(float(ymin)), int(float(xmax)), int(float(ymax))
                x1, y1, x2, y2, x3, y3, x4, y4 = xmin, ymin,xmin, ymax,xmax, ymax,xmax,ymin
            else:

                print(label)
                cx, cy, w, h ,angle = item.find('robndbox/cx').text,item.find('robndbox/cy').text,item.find('robndbox/w').text,item.find('robndbox/h').text,item.find('robndbox/angle').text
                cx, cy, w, h, angle = float(cx), float(cy), float(w), float(h),float(angle)
                # convert
                x = cx - w / 2
                y = cy - h / 2
                if angle < 1.57:
                    theta = round(angle, 6)
                else:
                    theta = round(angle - np.pi, 6)
                x1, y1, x2, y2, x3, y3, x4, y4 = rec_rotate(x, y, w, h, theta)
                x1, y1, x2, y2, x4, y4, x3, y3 = int(x1), int(y1), int(x2), int(y2), int(x4), int(y4), int(x3), int(y3)

            ann = [x1, y1, x2, y2, x3, y3, x4, y4, label, 1]
            ann = [str(item) for item in ann]
            ann_list.append(' '.join(ann))
            print (label, label, x1, y1, x2, y2, x3, y3, x4, y4)

        f.write('\n'.join(ann_list))

if __name__ ==  '__main__':
    xml_files = os.listdir('/home/solid/CD/ciomp/SAR/roxml') # xml
    os.makedirs('/home/solid/CD/ciomp/SAR/txt', exist_ok=True)    # txt
    for file in xml_files:
        convert_XML_to_DOTA(os.path.join('/home/solid/CD/ciomp/SAR/roxml', file))    # xml
