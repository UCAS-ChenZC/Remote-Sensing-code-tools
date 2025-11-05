import os
import pandas as pd

def count_phrases_in_txt_files(directory, phrases):
    # 初始化一个空的列表，用于收集所有文件的统计结果
    results_list = []

    # 确保提供的路径存在
    if not os.path.exists(directory):
        print("提供的目录不存在")
        return None  # 返回None或适当的值以表示错误

    # 遍历目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件扩展名是否为.txt
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                # 只提取文件名（不包含扩展名）
                file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
                # 打开并读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read().lower()  # 转换为小写进行不区分大小写的匹配
                    file_results = {phrase: contents.count(phrase.lower()) for phrase in phrases}
                    # 合并文件名和词组计数字典
                    file_data = {'File': file_name_without_ext, **file_results}
                    # 将合并后的字典添加到列表中
                    results_list.append(file_data)

    # 使用列表一次性创建DataFrame
    results_df = pd.DataFrame(results_list)

    # 保存到CSV文件
    csv_filename = os.path.join(directory, 'phrase_counts.csv')
    results_df.to_csv(csv_filename, index=False)

    print(f"统计结果已保存到 {csv_filename}")

    return results_df  # 返回DataFrame

# 使用示例
# 替换下面的路径为你的文件夹路径
directory_path = '/home/solid/可视化汇总1/回填第二波/txt'
# 定义你想统计的词组列表
phrases_to_count = [
    'Dump_Truck', 'Van', 'Small_Car', 'Cargo_Truck',
    'other-vehicle', 'Bus', 'Trailer', 'Truck_Tractor',
    'Excavator', 'Small'
]

# 调用函数
df = count_phrases_in_txt_files(directory_path, phrases_to_count)
