import os

# 指定要处理的文件夹路径
folder_path = '/path/to/your/folder'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件名是否以'..xml'结尾
    if filename.endswith('..xml'):
        # 创建新的文件名，将'..xml'替换为'.xml'
        new_filename = filename[:-5] + '.xml'
        
        # 生成完整的文件路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {old_file_path} to {new_file_path}')

print('重命名完成。')

