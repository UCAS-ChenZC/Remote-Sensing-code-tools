import os
import cv2
import xml.etree.ElementTree as ET

# 定义类别和对应的颜色
class_colors = {
    'Dump Truck': (255, 0, 0),  # 红色
    'Van': (0, 255, 0),  # 绿色
    'Small Car': (0, 0, 255),  # 蓝色
    'Cargo Truck': (255, 255, 0),  # 黄色
    'other-vehicle': (255, 165, 0),  # 橙色
    'Bus': (255, 255, 255),  # 白色
    'Trailer': (128, 0, 128),  # 紫色
    'Truck Tractor': (0, 128, 128),  # 青色
    'Excavator': (0, 255, 255),  # 绿色
    'Tractor': (128, 128, 0)  # 橄榄色
}

def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objects = []
    for obj in root.findall('objects/object'):
        coordinate = obj.find('coordinate').text
        type = obj.find('type').text
        description = obj.find('description').text
        possibleresult = obj.find('possibleresult')
        name = possibleresult.find('name').text
        probability = possibleresult.find('probability').text

        points = []
        for point in obj.find('points'):
            point_text = point.text.strip()
            x = float(point_text.split(',')[0])
            y = float(point_text.split(',')[1])
            points.append((int(x), int(y)))

        objects.append({
            'coordinate': coordinate,
            'type': type,
            'description': description,
            'name': name,
            'probability': float(probability),
            'points': points
        })
    return objects


def draw_objects(image_path, objects):
    image = cv2.imread(image_path)
    for obj in objects:
        points = obj['points']
        if obj['type'] == 'rectangle':
            color = class_colors.get(obj['name'], (0, 255, 0))  # 默认为绿色
            for i in range(len(points)):
                start_point = points[i]
                end_point = points[(i + 1) % len(points)]
                cv2.line(image, start_point, end_point, color, 1)
            text = f"{obj['name']}: {obj['probability']:.4f}"
            top_left = min(points, key=lambda x: (x[1], x[0]))
            cv2.putText(image, text, (top_left[0], top_left[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    return image


def process_images(input_image_folder, input_xml_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image_file in os.listdir(input_image_folder):
        if image_file.lower().endswith((".tif", ".jpg", ".png")):
            image_path = os.path.join(input_image_folder, image_file)
            xml_file = os.path.join(input_xml_folder, image_file.replace(image_file.split('.')[-1], 'xml'))

            if os.path.exists(xml_file):
                objects = parse_xml(xml_file)
                image_with_objects = draw_objects(image_path, objects)
                output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + '.png')
                cv2.imwrite(output_path, image_with_objects)
                print(f"Processed {image_file} -> {output_path}")
            else:
                print(f"XML file not found for {image_file}")

if __name__ == "__main__":
    # input_image_folder = '../input_path'
    # input_xml_folder = '../output_path'
    # output_folder = '../output_vis'
    input_image_folder = '/home/solid/TZ/dataset/fair1m_clean/images'
    input_xml_folder = '/home/solid/TZ/dataset/fair1m_clean/labels_xml'
    output_folder = '/home/solid/TZ/dataset/fair1m_clean/vis'
    process_images(input_image_folder, input_xml_folder, output_folder)









# import os
# import cv2
# import xml.etree.ElementTree as ET
#
# # 定义类别和对应的颜色
# class_colors = {
#     'Dump Truck': (255, 0, 0),  # 红色
#     'Van': (0, 255, 0),  # 绿色
#     'Small Car': (0, 0, 255),  # 蓝色
#     'Cargo Truck': (255, 255, 0),  # 黄色
#     'other-vehicle': (255, 165, 0),  # 橙色
#     'Bus': (255, 255, 255),  # 白色
#     'Trailer': (128, 0, 128),  # 紫色
#     'Truck Tractor': (0, 128, 128),  # 青色
#     'Excavator': (0, 255, 255),  # 绿色
#     'Tractor': (128, 128, 0)  # 橄榄色
# }
#
#
# def parse_xml(xml_path):
#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#     objects = []
#     for obj in root.findall('objects/object'):
#         coordinate = obj.find('coordinate').text
#         type = obj.find('type').text
#         description = obj.find('description').text
#         name = obj.find('possibleresult/name').text
#
#         points = []
#         for point in obj.findall('points/point'):
#             point_text = point.text.strip()
#             x = float(point_text.split(',')[0])
#             y = float(point_text.split(',')[1])
#             points.append((int(x), int(y)))
#
#         objects.append({
#             'coordinate': coordinate,
#             'type': type,
#             'description': description,
#             'name': name,
#             'points': points
#         })
#     return objects
#
# def draw_objects(image_path, objects):
#     image = cv2.imread(image_path)
#     for obj in objects:
#         points = obj['points']
#         color = class_colors.get(obj['name'], (0, 255, 0))  # 默认为绿色
#
#         # 绘制四点框
#         for i in range(len(points)):
#             start_point = points[i]
#             end_point = points[(i + 1) % len(points)]
#             cv2.line(image, start_point, end_point, color, 2)
#
#         # 绘制文本
#         text = f"{obj['name']}"
#         top_left = min(points, key=lambda x: (x[1], x[0]))
#         cv2.putText(image, text, (top_left[0], top_left[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#
#     return image
#
# def process_images(input_image_folder, input_xml_folder, output_folder):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#
#     for image_file in os.listdir(input_image_folder):
#         if image_file.lower().endswith((".tif", ".jpg", ".png")):
#             image_path = os.path.join(input_image_folder, image_file)
#             xml_file = os.path.join(input_xml_folder, image_file.replace(image_file.split('.')[-1], 'xml'))
#
#             if os.path.exists(xml_file):
#                 objects = parse_xml(xml_file)
#                 image_with_objects = draw_objects(image_path, objects)
#                 output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + '.png')
#                 cv2.imwrite(output_path, image_with_objects)
#                 print(f"Processed {image_file} -> {output_path}")
#             else:
#                 print(f"XML file not found for {image_file}")
#
# if __name__ == "__main__":
#     input_image_folder = '/home/solid/TZ/dataset/car_det_train/images'
#     input_xml_folder = '/home/solid/TZ/dataset/car_det_train/gt'
#     output_folder = '/home/solid/TZ/dataset/car_det_train/vis'
#
#     process_images(input_image_folder, input_xml_folder, output_folder)