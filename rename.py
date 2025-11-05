import os
import re

def replace_whole_word(input_path, output_path):
    # 确保输出路径存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # 定义替换规则
    replace_rules = {
        #r'\bOther_Vehicle\b': 'other-vehicle',
        #r'\bOther-Vehicle\b': 'other-vehicle',
        #r'\bOther-vehicle\b': 'other-vehicle',
        #r'\bV\b': 'Van',
        #r'\bSmall\b': 'Small_Car',
        #r'\bSamll_Car\b': 'Small_Car',  # 假设这是拼写错误，修正为正确的形式
        #r'\bSamll_CAr\b': 'Small_Car',  # 这里看起来是重复的，可能不需要
        #r'\bSm\b': 'Small_Car',  # 假设这是'Small Car'的缩写
        #r'\bCargo\b': 'Cargo_Truck',
        #r'\bDupm_Truck\b': 'Dump_Truck',
        #r'\bTruck Tractor\b': 'Truck_Tractor',
        r'\bcar\b': 'Small_Car'
    }
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_path):
        if filename.endswith('.txt'):
            # 构建完整的文件路径
            input_file_path = os.path.join(input_path, filename)
            output_file_path = os.path.join(output_path, filename)
            
            # 读取文件内容
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 对每个规则执行替换操作
            for old, new in replace_rules.items():
                content = re.sub(old, new, content)
            
            # 写入新内容到输出文件
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
    
    print(f"All '.txt' files have been processed and saved to {output_path}")

# 使用示例
input_folder = ''  # 替换为你的输入文件夹路径
output_folder = ''  # 替换为你的输出文件夹路径
replace_whole_word(input_folder, output_folder)
#检索文件夹下txt中的标签名，输出标签名只为'Truck'的文件名，而不是标签名含有'Truck'的555555555555552555555555
