import os

def find_files_with_only_exact_category(directory, exact_category_name):
    """
    遍历指定目录中的 .txt 文件，找出其中唯一标签名完全是指定类别名的文件。

    :param directory: 需要遍历的目录路径
    :param exact_category_name: 需要查找的完全匹配的类别名
    :return: 包含唯一标签名为指定类别名的文件名称列表
    """
    matched_files = []

    # 遍历目录中的文件
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)

                # 打开文件并检查内容
                with open(file_path, 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    
                    # 检查是否只有一个标签名，并且是完全匹配的类别名
                    if len(lines) == 1 and lines[0] == exact_category_name:
                        matched_files.append(filename)

    return matched_files

# 使用示例
directory_path = '/home/solid/可视化汇总1/回填第二波/txt'
exact_category_name = 'Small_Car'
files_with_only_exact_category = find_files_with_only_exact_category(directory_path, exact_category_name)

print("Files containing only the exact category '{}':".format(exact_category_name))
for file in files_with_only_exact_category:
    print(file)

