import cv2
import numpy as np
import os

#visiualize the txt label on the image

# 定义颜色映射表，每个类别对应一种颜色
class_colors = [
    (255, 0, 0),  # 红色
    (0, 255, 0),  # 绿色
    (0, 0, 255),  # 蓝色
    (255, 255, 0),  # 黄色
    (255, 0, 255),  # 品红
    (0, 255, 255),  # 青色
    (192, 192, 192),  # 灰色
    (128, 0, 128),  # 紫色
    (128, 128, 0),  # 橄榄色
    (0, 128, 128)  # 深青色
]

def read_labels_from_file(labels_path):
    with open(labels_path, 'r') as file:
        labels = file.readlines()
    return labels

def draw_polygon_and_label_on_image(image, points, label_class, class_index, thickness=1, font_scale=0.5):
    # 根据类别索引选择颜色
    color = class_colors[class_index % len(class_colors)]

    # 将点列表转换为NumPy数组，用于绘制多边形
    points = np.array(points, dtype=np.int32)
    cv2.polylines(image, [points], isClosed=True, color=color, thickness=thickness)

    # 在多边形旁边绘制文本标注
    label_position = (points[0][0], points[0][1] - 10)  # 假设文本标注放在第一个点的上方
    cv2.putText(image, label_class, label_position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

def main(input_image_folder, input_labels_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入图像文件夹中的所有文件
    for filename in os.listdir(input_image_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(input_image_folder, filename)
            labels_filename = filename.replace(".png", ".txt")
            labels_path = os.path.join(input_labels_folder, labels_filename)

            # 检查对应的标签文件是否存在
            if not os.path.exists(labels_path):
                print(f"No corresponding label file found for {filename}, skipping...")
                continue

            # 读取图像
            image = cv2.imread(image_path)
            if image is None:
                print(f"Image could not be read: {image_path}")
                continue

            # 读取标签
            labels = read_labels_from_file(labels_path)

            # 绘制多边形框和标签
            for label in labels:
                parts = label.strip().split()
                # 提取坐标和标签类别
                points = [(int(parts[i]), int(parts[i + 1])) for i in range(0, 8, 2)]
                label_class = parts[-2]  # 标签类别是倒数第二个值
                # 假设类别索引是类别名称的ASCII码和，这里需要根据实际情况来确定类别索引
                label_index = sum(ord(c) for c in label_class)
                draw_polygon_and_label_on_image(image, points, label_class, label_index)

            # 保存图像
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)

if __name__ == "__main__":
    # 替换为你的图像路径、标签文件路径和输出路径
    input_image_folder = ''
    input_labels_folder = ''
    output_folder = ''

    # 执行主函数
    main(input_image_folder, input_labels_folder, output_folder)
