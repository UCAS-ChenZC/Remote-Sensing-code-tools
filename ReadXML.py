# 文件夹路径
#folder_path = '/home/solid/CAR/output_path/2073-output_path'
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

# 文件夹路径
folder_path = '/home/solid/CAR/output_path/allin69_0.1-output_path'

# 存储每个类别的阈值
category_thresholds = defaultdict(list)

# 遍历文件夹下的所有XML文件
for filename in os.listdir(folder_path):
    if filename.endswith('.xml'):
        file_path = os.path.join(folder_path, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 遍历XML文件中的所有对象
        for obj in root.findall('objects/object'):
            category = obj.find('possibleresult/name').text
            threshold = float(obj.find('possibleresult/probability').text)
            category_thresholds[category].append(threshold)

# 计算每个类别的平均阈值、最高阈值和最低阈值
for category, thresholds in category_thresholds.items():
    avg_threshold = sum(thresholds) / len(thresholds)
    max_threshold = max(thresholds)
    min_threshold = min(thresholds)
    
    print(f'类别: {category}')
    print(f'平均阈值: {avg_threshold}')
    print(f'最高阈值: {max_threshold}')
    print(f'最低阈值: {min_threshold}')
    print('---------------------------------------')
