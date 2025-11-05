
"""删除非同名"""
import os


def get_base_name(path):
    """
    从路径中获取文件名（不包含扩展名）
    """
    name, ext = os.path.splitext(os.path.basename(path))
    return name


def delete_non_matching_files(folder1, folder2):
    """
    删除文件夹内非同名的文件
    """
    # 获取文件夹内所有文件
    files1 = {get_base_name(file): file for file in os.listdir(folder1)}
    files2 = {get_base_name(file): file for file in os.listdir(folder2)}

    # 获取两个文件夹文件名的交集
    common_files = files1.keys() & files2.keys()

    # 删除folder1中非同名文件
    for name, file in files1.items():
        if name not in common_files:
            os.remove(os.path.join(folder1, file))
            print(f"Deleted from {folder1}: {file}")

    # 删除folder2中非同名文件
    for name, file in files2.items():
        if name not in common_files:
            os.remove(os.path.join(folder2, file))
            print(f"Deleted from {folder2}: {file}")


if __name__ == "__main__":
    folder1 = '/home/solid/CD/code/BCD/Duibishiyan/C_img/Edge_LEVIR/new'
    folder2 = '/home/solid/CD/code/BCD/Duibishiyan/C_img/Edge_LEVIR/C_511Ours'

    if os.path.isdir(folder1) and os.path.isdir(folder2):
        delete_non_matching_files(folder1, folder2)
    else:
        print("One or both paths are not valid directories.")
