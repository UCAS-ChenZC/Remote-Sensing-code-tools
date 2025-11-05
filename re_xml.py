from lxml import etree
import os

# 定义您想要保留的类别列表
desired_categories = [
    'Dump Truck',
    'Van',
    'Small Car',
    'Cargo Truck',
    'other-vehicle',
    'Bus',
    'Trailer',
    'Truck Tractor',
    'Excavator',
    'Tractor'
]

# 输入文件夹路径
input_folder_path = '/home/solid/TZ/PETDet-dev/work_dirs/Task1_results(0.4)'
# 输出文件夹路径
output_folder_path = '/home/solid/TZ/PETDet-dev/work_dirs/Task1_results(0.4)/re_xml'

# 确保输出文件夹存在
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder_path):
    if filename.endswith('.xml'):
        # 构建XML文件的完整路径
        xml_file_path = os.path.join(input_folder_path, filename)

        # 解析XML文件
        tree = etree.parse(xml_file_path)
        root = tree.getroot()

        # 找到所有的<object>元素
        objects = root.findall('.//object')

        # 遍历所有<object>元素，并过滤<name>元素
        for obj in objects:
            possibleresult = obj.find('possibleresult')
            if possibleresult is not None:
                name_elem = possibleresult.find('name')
                # 如果<name>元素的文本不在desired_categories列表中，则删除整个<object>元素
                if name_elem is not None and name_elem.text not in desired_categories:
                    obj.getparent().remove(obj)

        # 构建输出文件的完整路径，使用原始文件名
        output_file_path = os.path.join(output_folder_path, filename)

        # 将修改后的XML文件写入到输出路径
        tree.write(output_file_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

        print(f'Filtered XML file has been saved to {output_file_path}')


