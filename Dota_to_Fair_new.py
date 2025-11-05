import os
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageFile
from xml.dom import minidom
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# 增加像素限制
Image.MAX_IMAGE_PIXELS = 1000000000  # 或者设定一个合理的最大值，如 10 亿像素
ImageFile.LOAD_TRUNCATED_IMAGES = True  # 允许加载被截断的图像

# 通用函数：根据图像模式确定深度
def get_image_depth(image):
    mode_to_depth = {
        '1': 1,    # 1-bit pixels, black and white
        'L': 1,    # 8-bit pixels, grayscale
        'P': 1,    # 8-bit pixels, mapped to any other mode using a color palette
        'RGB': 3,  # 3x8-bit pixels, true color
        'RGBA': 4, # 4x8-bit pixels, true color with transparency
        'CMYK': 4, # 4x8-bit pixels, color separation
        'YCbCr': 3,# 3x8-bit pixels, color video format
        'I': 1,    # 32-bit signed integer pixels
        'F': 1     # 32-bit floating point pixels
    }
    return mode_to_depth.get(image.mode, 3)  # 默认RGB深度为3

def txt_to_xml(txt_file_path, image_file_path, xml_file_path):
    # 打开图像文件以获取尺寸
    try:
        with Image.open(image_file_path) as img:
            image_width, image_height = img.size
            image_depth = get_image_depth(img)
    except Exception as e:
        logging.error(f"打开图像文件 {image_file_path} 失败: {e}")
        return

    # 创建XML根元素
    annotation = ET.Element("annotation")
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "filename").text = os.path.basename(image_file_path)
    ET.SubElement(source, "origin").text = "Optical"
    # 添加research元素
    research = ET.SubElement(annotation, "research")
    ET.SubElement(research, "version").text = "1.0"
    ET.SubElement(research, "author").text = "Cyber"
    ET.SubElement(research, "pluginclass").text = "object detection"
    ET.SubElement(research, "time").text = "2021-07-21"
    # 添加size元素
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(image_width)
    ET.SubElement(size, "height").text = str(image_height)
    ET.SubElement(size, "depth").text = str(image_depth)  # 动态设置深度

    objects = ET.SubElement(annotation, "objects")

    # 读取txt文件并创建object元素
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 9:  # 确保有足够的数据
                try:
                    x1, y1, x2, y2, x3, y3, x4, y4, class_name, _ = parts
                    # 验证坐标是否合法
                    coordinates = [int(float(x)) for x in [x1, y1, x2, y2, x3, y3, x4, y4]]
                    if any(c < 0 for c in coordinates) or \
                       any(c >= image_width for c in [coordinates[0], coordinates[2]] if c >= image_width) or \
                       any(c >= image_height for c in [coordinates[1], coordinates[3]] if c >= image_height):
                        logging.warning(f"坐标超出图像范围: {line.strip()}")
                        continue

                    object_elem = ET.SubElement(objects, "object")
                    ET.SubElement(object_elem, "coordinate").text = "pixel"
                    ET.SubElement(object_elem, "type").text = "rectangle"
                    ET.SubElement(object_elem, "description").text = "None"
                    possibleresult = ET.SubElement(object_elem, "possibleresult")
                    ET.SubElement(possibleresult, "name").text = class_name

                    points = ET.SubElement(object_elem, "points")
                    ET.SubElement(points, "point").text = f"{coordinates[0]},{coordinates[1]}"
                    ET.SubElement(points, "point").text = f"{coordinates[2]},{coordinates[3]}"
                    ET.SubElement(points, "point").text = f"{coordinates[4]},{coordinates[5]}"
                    ET.SubElement(points, "point").text = f"{coordinates[6]},{coordinates[7]}"
                    ET.SubElement(points, "point").text = f"{coordinates[0]},{coordinates[1]}"  # 闭环

                except Exception as e:
                    logging.error(f"处理行 {line.strip()} 失败: {e}")

    # 使用minidom美化XML字符串
    xmlstr = ET.tostring(annotation, 'utf-8')
    pretty_xml = minidom.parseString(xmlstr).toprettyxml(indent="\t")

    # 写入XML文件
    try:
        with open(xml_file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
    except Exception as e:
        logging.error(f"写入XML文件 {xml_file_path} 失败: {e}")

# 支持的图片格式
supported_image_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']

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
        
        # 从txt文件名中提取图像文件名，并检查支持的图像格式
        base_image_name = os.path.splitext(txt_file)[0]
        image_file_path = None
        
        # 尝试查找不同格式的图像文件
        for ext in supported_image_formats:
            image_candidate = os.path.join(image_folder_path, base_image_name + ext)
            if os.path.isfile(image_candidate):
                image_file_path = image_candidate
                break
        
        # 如果没有找到图像文件，跳过该标签文件
        if image_file_path is None:
            logging.warning(f"未找到与 {txt_file_path} 对应的图像文件，跳过该标签文件。")
            continue

        # 构建XML文件的完整路径
        xml_file_name = os.path.splitext(txt_file)[0] + '.xml'
        xml_file_path = os.path.join(xml_output_path, xml_file_name)

        # 执行转换
        txt_to_xml(txt_file_path, image_file_path, xml_file_path)

logging.info("转换完成。")

