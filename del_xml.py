import os
import xml.etree.ElementTree as ET

"""根据置信度删除xml"""

def remove_low_probability_objects(input_path, output_path):
    # 确保输入路径存在
    if not os.path.exists(input_path):
        print(f"The directory {input_path} does not exist.")
        return False

    # 确保输出路径存在，如果不存在则创建
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 遍历输入路径下的所有文件
    for filename in os.listdir(input_path):
        if filename.endswith('.xml'):
            # 构造完整的文件路径
            file_path = os.path.join(input_path, filename)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # 找到<objects>元素
            objects_elem = root.find('objects')
            if objects_elem is not None:
                # 找到所有的<object>元素
                objects = objects_elem.findall('object')
                for obj in objects:
                    # 获取<probability>元素
                    probability_elem = obj.find('possibleresult/probability')
                    if probability_elem is not None:
                        # 将概率值转换为浮点数
                        probability = float(probability_elem.text)
                        # 如果概率小于0.5，则删除该<object>
                        if probability < 0.6:
                            objects_elem.remove(obj)

            # 构造输出文件的完整路径
            output_file_path = os.path.join(output_path, filename)
            # 写入修改后的XML到输出文件
            tree.write(output_file_path, encoding='utf-8', xml_declaration=True)
            print(f"File processed and saved: {output_file_path}")

    return True

# 使用示例
input_directory = ''
output_directory = ''
remove_low_probability_objects(input_directory, output_directory)