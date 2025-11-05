import os

def replace_underscore(input_path, output_path):
    # 确保输出路径存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_path):
        if filename.endswith('.txt'):
            # 构建完整的文件路径
            input_file_path = os.path.join(input_path, filename)
            output_file_path = os.path.join(output_path, filename)
            
            # 读取文件内容
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 替换空格为下划线
            '''updated_content = content.replace('p T', 'p_T')
            updated_content = updated_content.replace('l C', 'l_C')
            updated_content = updated_content.replace('o T', 'o_T')
            updated_content = updated_content.replace('k T', 'k_T')'''
            #替换下划线为空格
            updated_content = content.replace('p_T', 'p T')
            updated_content = updated_content.replace('l_C', 'l C')
            updated_content = updated_content.replace('o_T', 'o T')
            updated_content = updated_content.replace('k_T', 'k T')
                    
            # 写入新内容到输出文件
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
    
    print(f"All '.txt' files have been processed and saved to {output_path}")

# 使用示例
input_folder = '/home/solid/可视化汇总1/pingfen_txt'  # 替换为你的输入文件夹路径
output_folder = '/home/solid/可视化汇总1/pingfen_txt1'  # 替换为你的输出文件夹路径
replace_underscore(input_folder, output_folder)
