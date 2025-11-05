import os
import math
from xml.etree import ElementTree as ET

def rotated_box_to_points(cx, cy, w, h, angle):
    """
    将旋转框 (cx, cy, w, h, angle) 转换为 4 个顶点 (x1,y1,...,x4,y4)
    """
    angle = -float(angle)  # 顺时针旋转为负
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    dx = w / 2.0
    dy = h / 2.0

    points = []
    for x, y in [(-dx, -dy), (dx, -dy), (dx, dy), (-dx, dy)]:
        px = cx + x * cos_a - y * sin_a
        py = cy + x * sin_a + y * cos_a
        points.append((px, py))
    return points

def convert_XML_to_DOTA(filename, out_dir):
    tree = ET.parse(filename)
    root = tree.getroot()
    objects = root.findall('object')
    base_name = os.path.splitext(os.path.basename(filename))[0]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, base_name + '.txt')

    with open(out_path, 'w') as f:
        for obj in objects:
            name = obj.find('name').text
            robndbox = obj.find('robndbox')
            if robndbox is None:
                continue
            cx = float(robndbox.find('cx').text)
            cy = float(robndbox.find('cy').text)
            w = float(robndbox.find('w').text)
            h = float(robndbox.find('h').text)
            angle = float(robndbox.find('angle').text)

            points = rotated_box_to_points(cx, cy, w, h, angle)
            coords = [str(round(p[0], 2)) + ' ' + str(round(p[1], 2)) for p in points]
            flat_coords = ' '.join([str(round(c, 2)) for point in points for c in point])
            f.write(f"{flat_coords} {name} 1\n")

if __name__ == '__main__':
    input_dir = '/media/solid/T9/CZC/506/22/label'  # 存放 XML 的路径
    output_dir = '/media/solid/T9/CZC/506/22/txt'   # 输出 TXT 的路径
    os.makedirs(output_dir, exist_ok=True)

    for xml_file in os.listdir(input_dir):
        if xml_file.endswith('.xml'):
            convert_XML_to_DOTA(os.path.join(input_dir, xml_file), output_dir)

