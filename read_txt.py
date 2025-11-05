import os
import pandas as pd
from collections import defaultdict

# 假设每个txt文件中，每行代表一个类别及其数量，例如 "类别A 10"
def parse_line_to_tag_count(line):
    parts = line.strip().split()
    if len(parts) == 2:
        tag, count = parts
        return tag, int(count)
    return None, None

def count_tags_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tag_counts = defaultdict(int)  # 使用defaultdict来计数每个标签的出现次数
        for line in file:
            tag, count = parse_line_to_tag_count(line)
            if tag and count is not None:
                tag_counts[tag] += count
    return dict(tag_counts)  # 将defaultdict转换为普通字典

folder_path = '/home/solid/yolo自回填/test/labels/train_original'  # 替换为你的txt文件文件夹路径
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# 初始化DataFrame
df = pd.DataFrame(columns=['File Name', 'Category', 'Total Count'])

# 遍历txt文件，读取每个类别的总数，并添加到DataFrame中
for txt_file in txt_files:
    file_path = os.path.join(folder_path, txt_file)
    file_tag_counts = count_tags_in_file(file_path)
    for category, total_count in file_tag_counts.items():
        df = df.append({'File Name': txt_file, 'Category': category, 'Total Count': total_count}, ignore_index=True)

# 显示DataFrame
#print(df)

# 将表格保存为CSV文件
df.to_csv('categories_counts1.csv', index=False)
