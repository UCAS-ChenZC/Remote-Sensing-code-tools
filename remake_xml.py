import os
import shutil
import xml.etree.ElementTree as ET

# 原文件夹和新建文件夹路径
original_folder_path = '/media/solid/902EAC1C2EABF8FC/datasets/Space_Based_v9/val/test_val'
new_folder_path = '/media/solid/902EAC1C2EABF8FC/datasets/Space_Based_v9/val/111'

# 需要重命名的标签字典
rename_dict = {
    'Small_Car': 'Small Car',
    'Dump_Truck': 'Dump Truck',
    'Cargo_Truck': 'Cargo Truck',
    'Truck_Tractor': 'Truck Tractor'
}

# 创建新文件夹
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)

# 遍历原文件夹下的所有XML文件
for filename in os.listdir(original_folder_path):
    if filename.endswith('.xml'):
        original_file_path = os.path.join(original_folder_path, filename)
        new_file_path = os.path.join(new_folder_path, filename)

        shutil.copy(original_file_path, new_file_path)  # 复制未修改的文件到新文件夹

        tree = ET.parse(new_file_path)
        root = tree.getroot()

        # 遍历XML文件中的所有对象
        for obj in root.findall('objects/object'):
            category = obj.find('possibleresult/name').text

            # 如果标签需要重命名，则进行重命名
            if category in rename_dict:
                obj.find('possibleresult/name').text = rename_dict[category]

        # 保存修改后的XML文件，保持原始格式
        tree.write(new_file_path, encoding='utf-8', xml_declaration=True)

print("标签重命名完成。修改后的文件保存在新文件夹中。")
