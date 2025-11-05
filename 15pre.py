import cv2
import numpy as np
import os

# 路径设置
pred_dir = "filtered_output"     # 带红框的预测图（只包含可框区域的图像）
gt_dir = "ground_truths"         # 真值图（灰度图），文件名需一致

# 框大小
BOX_SIZE = 15
THRESHOLD = 0.3  # 如果区域中 ≥30% 像素为255，认为是真值中是变化区域

total_boxes = 0
correct_boxes = 0

results = []

# 遍历预测图
for filename in os.listdir(pred_dir):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif')):
        continue

    pred_path = os.path.join(pred_dir, filename)
    gt_path = os.path.join(gt_dir, filename)

    # 读取图像
    pred_img = cv2.imread(pred_path)
    gt_img = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)

    if pred_img is None or gt_img is None:
        print(f"跳过无法读取的图像：{filename}")
        continue

    height, width = gt_img.shape
    boxes_this_image = 0
    correct_this_image = 0

    # 提取红框区域（通过扫描红色像素线条）
    red_mask = (pred_img[:, :, 2] > 200) & (pred_img[:, :, 1] < 100) & (pred_img[:, :, 0] < 100)
    red_coords = np.column_stack(np.where(red_mask))

    # 获取所有红框左上角（找水平线+垂直线交点）
    checked = set()
    for y, x in red_coords:
        if (x, y) in checked:
            continue
        # 左上角像素位置为红框起点，检查是否超出边界
        if x + BOX_SIZE <= width and y + BOX_SIZE <= height:
            checked.add((x, y))
            box = gt_img[y:y + BOX_SIZE, x:x + BOX_SIZE]
            total = BOX_SIZE * BOX_SIZE
            changed = np.sum(box == 255)
            ratio = changed / total

            total_boxes += 1
            boxes_this_image += 1

            if ratio >= THRESHOLD:
                correct_boxes += 1
                correct_this_image += 1

    acc = correct_this_image / boxes_this_image if boxes_this_image > 0 else 0
    results.append((filename, boxes_this_image, correct_this_image, acc))

# 打印结果
print("\n📊 每张图像准确率：")
for name, total_b, correct_b, acc in results:
    print(f"{name}: 命中 {correct_b}/{total_b} 区域，准确率 = {acc:.2%}")

overall_acc = correct_boxes / total_boxes if total_boxes > 0 else 0
print(f"\n✅ 总体准确率（仅对可框区域）: {correct_boxes}/{total_boxes} = {overall_acc:.2%}")

