from xml.etree import ElementTree as ET  # xml文件解析方法
import numpy as np
import cv2
import os
import random
import math

def get_angle(x1, y1, x2, y2, x3, y3, x4, y4):
    if x2 - x1 != 0 and x4 - x3 != 0:
        theta = (math.atan((y2 - y1) / (x2 - x1)) + math.atan((y4 - y3) / (x4 - x3))) / 2
    else:
        theta = np.pi / 2

    if theta >= 0:
        angle = theta
    else:
        angle = theta + np.pi
    return angle, theta


def resize_vertices_different_aspect(x1, y1, x2, y2, x3, y3, x4, y4, scale_factor_w, scale_factor_h):
    # 计算新的顶点坐标
    x1_new, y1_new = x1 * scale_factor_w, y1 * scale_factor_h
    x2_new, y2_new = x2 * scale_factor_w, y2 * scale_factor_h
    x3_new, y3_new = x3 * scale_factor_w, y3 * scale_factor_h
    x4_new, y4_new = x4 * scale_factor_w, y4 * scale_factor_h

    return x1_new, y1_new, x2_new, y2_new, x3_new, y3_new, x4_new, y4_new


def get_w_and_h(x1, y1, x2, y2, x3, y3, x4, y4):
    w = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    h = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
    return int(w), int(h)


def get_x_and_y(x1, y1, x2, y2, x3, y3, x4, y4, theta, w, h):
    cx = (x2 + x3) / 2
    cy = (y2 + y3) / 2
    x = cx - w / 2
    y = cy - h / 2
    return x, y, cx, cy


def load_boxes(file_path):
    """
    Load bounding boxes from a text file.

    Args:
    file_path (str): The path to the file containing the bounding box annotations.

    Returns:
    list: A list of bounding boxes where each box is represented as a list [x_min, y_min, x_max, y_max].
    """
    boxes = []

    mydoc = ET.parse(file_path)
    root = mydoc.getroot()

    objects = root.find('objects')
    items = objects.find('object')
    output_file = os.path.splitext(os.path.split(file_path)[-1])[0] + '.txt'
    with open(f'file_path', 'w') as f:  # txt
        ann_list = []
        # for item in items:
        label = items.find('possibleresult')
        points = items.find('points')
        label = label.find('name').text
        mapped_label = label
        if mapped_label != 'ignore':
            points = [[int(float(item)) for item in point.text.split(',')] for point in points.findall('point')]
            x1, y1 = points[0]
            x2, y2 = points[1]
            x3, y3 = points[2]
            x4, y4 = points[3]

        boxes.append([x1, y1, x2, y2, x3, y3, x4, y4, mapped_label])
    return boxes


# （3）处理超出边缘的检测框
def merge_bboxes(bboxes, cutx, cuty):
    # 保存修改后的检测框
    merge_box = []

    # 遍历每张图像，共4个
    for i, box in enumerate(bboxes):

        # 每张图片中需要删掉的检测框
        index_list = []

        # 遍历每张图的所有检测框,index代表第几个框
        for index, box in enumerate(box[0]):

            # axis=1纵向删除index索引指定的列，axis=0横向删除index指定的行
            # box[0] = np.delete(box[0], index, axis=0)

            # 获取每个检测框的宽高
            x1, y1, x2, y2, x3, y3, x4, y4, label = box
            xlist = [x1, x2, x3, x4]
            ylist = [y1, y2, y3, y4]
            max_x = int(max(xlist))
            min_x = int(min(xlist))
            max_y = int(max(ylist))
            min_y = int(min(ylist))
            # 如果是左上图，修正右侧和下侧框线
            if i == 0:
                # 如果检测框左上坐标点不在第一部分中，就忽略它
                if max_x > (cutx + 5) or max_y > (cuty + 5):
                    index_list.append(index)

            #             # 如果是右上图，修正左侧和下册框线
            if i == 1:
                if min_x < (cutx - 5) or max_y > (cuty + 5):
                    index_list.append(index)

            #             # 如果是左下图
            if i == 2:
                if max_x > (cutx + 5) or min_y < (cuty - 5):
                    index_list.append(index)

            #             # 如果是右下图
            if i == 3:
                if min_x < cutx or min_y < cuty:
                    index_list.append(index)

        # 删除不满足要求的框，并保存
        merge_box.append(np.delete(bboxes[i][0], index_list, axis=0))

    # 返回坐标信息
    return merge_box


# （1）对传入的四张图片数据增强
def get_random_data(image_list, input_shape):
    h, w = input_shape  # 获取图像的宽高

    '''设置拼接的分隔线位置'''
    min_offset_x = 0.4
    min_offset_y = 0.4
    scale_low = 1 - min(min_offset_x, min_offset_y)  # 0.6
    scale_high = scale_low + 0.2  # 0.8

    image_datas = []  # 存放图像信息
    box_datas = []  # 存放检测框信息
    index = 0  # 当前是第几张图

    # （1）图像分割
    for index, frame_list in enumerate(image_list):

        frame = frame_list[0]  # 取出的某一张图像
        box = np.array(frame_list[1:])  # 该图像对应的检测框坐标
        label = box[-1]

        ih, iw = frame.shape[0:2]  # 图片的宽高
        x1, y1, x2, y2, x3, y3, x4, y4 = int(box[0, :, 0][0]), int(box[0, :, 1][0]), int(box[0, :, 2][0]), int(
            box[0, :, 3][0]), int(box[0, :, 4][0]), int(box[0, :, 5][0]), int(box[0, :, 6][0]), int(box[0, :, 7][0])

        # 对输入图像缩放
        new_ar = w / h  # 图像的宽高比
        scale = np.random.uniform(scale_low, scale_high)  # 缩放0.6--0.8倍
        # 调整后的宽高
        nh = int(scale * h)  # 缩放比例乘以要求的宽高
        nw = int(nh * new_ar)  # 保持原始宽高比例

        # 缩放图像
        frame = cv2.resize(frame, (nw, nh))

        x1, y1, x2, y2, x3, y3, x4, y4 = resize_vertices_different_aspect(x1, y1, x2, y2, x3, y3, x4, y4, nw / iw,
                                                                          nh / ih)

        # 创建一块[416,416]的底版
        new_frame = np.zeros((h, w, 3), np.uint8)

        # 确定每张图的位置
        if index == 0:
            new_frame[0:nh, 0:nw] = frame  # 第一张位于左上方
        elif index == 1:
            new_frame[0:nh, w - nw:w] = frame  # 第二张位于右上方
        elif index == 2:
            new_frame[h - nh:h, 0:nw] = frame  # 第三张位于左下方
        elif index == 3:
            new_frame[h - nh:h, w - nw:w] = frame  # 第四张位于右下方

        # 修正每个检测框的位置
        if index == 0:  # 左上图像
            box[0, :, 0][0] = int(x1)
            box[0, :, 1][0] = int(y1)
            box[0, :, 2][0] = int(x2)
            box[0, :, 3][0] = int(y2)
            box[0, :, 4][0] = int(x3)
            box[0, :, 5][0] = int(y3)
            box[0, :, 6][0] = int(x4)
            box[0, :, 7][0] = int(y4)
        if index == 1:  # 右上图像
            box[0, :, 0][0] = int(x1) + w - nw
            box[0, :, 1][0] = int(y1)
            box[0, :, 2][0] = int(x2) + w - nw
            box[0, :, 3][0] = int(y2)
            box[0, :, 4][0] = int(x3) + w - nw
            box[0, :, 5][0] = int(y3)
            box[0, :, 6][0] = int(x4) + w - nw
            box[0, :, 7][0] = int(y4)
        if index == 2:  # 右上图像
            box[0, :, 0][0] = int(x1)
            box[0, :, 1][0] = int(y1) + h - nh
            box[0, :, 2][0] = int(x2)
            box[0, :, 3][0] = int(y2) + h - nh
            box[0, :, 4][0] = int(x3)
            box[0, :, 5][0] = int(y3) + h - nh
            box[0, :, 6][0] = int(x4)
            box[0, :, 7][0] = int(y4) + h - nh
        if index == 3:  # 右上图像
            box[0, :, 0][0] = int(x1) + w - nw
            box[0, :, 1][0] = int(y1) + h - nh
            box[0, :, 2][0] = int(x2) + w - nw
            box[0, :, 3][0] = int(y2) + h - nh
            box[0, :, 4][0] = int(x3) + w - nw
            box[0, :, 5][0] = int(y3) + h - nh
            box[0, :, 6][0] = int(x4) + w - nw
            box[0, :, 7][0] = int(y4) + h - nh

        # 保存处理后的图像及对应的检测框坐标
        image_datas.append(new_frame)
        box_datas.append(box)

    for image, boxes in zip(image_datas, box_datas):
        # 复制一份原图
        image_copy = image.copy()
        bbox_ = boxes[0, 0, :]
        bbox = []
        bbox.append((int(bbox_[0]), int(bbox_[1])))
        bbox.append((int(bbox_[2]), int(bbox_[3])))
        bbox.append((int(bbox_[4]), int(bbox_[5])))
        bbox.append((int(bbox_[6]), int(bbox_[7])))

        # 可视化
        # cv2.putText(image_copy, bbox_[-1], (int(bbox_[0]), int(bbox_[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),
        #             2)
        # cv2.line(image_copy, bbox[0], bbox[1], (0, 0, 255), 1, 4)
        # cv2.line(image_copy, bbox[1], bbox[2], (0, 0, 255), 1, 4)
        # cv2.line(image_copy, bbox[2], bbox[3], (0, 0, 255), 1, 4)
        # cv2.line(image_copy, bbox[3], bbox[0], (0, 0, 255), 1, 4)
        #
        # cv2.imshow('img', image_copy)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # （2）将四张图像拼接在一起
    # 在指定范围中选择横纵向分割线
    cutx = np.random.randint(int(w * min_offset_x), int(w * (1 - min_offset_x)))
    cuty = np.random.randint(int(h * min_offset_y), int(h * (1 - min_offset_y)))

    # 创建一块[416,416]的底版用来组合四张图
    new_image = np.zeros((h, w, 3), np.uint8)
    new_image[:cuty, :cutx, :] = image_datas[0][:cuty, :cutx, :]
    new_image[:cuty, cutx:, :] = image_datas[1][:cuty, cutx:, :]
    new_image[cuty:, :cutx, :] = image_datas[2][cuty:, :cutx, :]
    new_image[cuty:, cutx:, :] = image_datas[3][cuty:, cutx:, :]

    # 显示合并后的图像
    # cv2.imshow('new_img', new_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 复制一份合并后的原图
    final_image_copy = new_image.copy()

    # 显示有检测框并合并后的图像
    for boxes in box_datas:

        # 遍历该张图像中的所有检测框
        for box in boxes[0]:
            bbox_ = box
            bbox = []
            bbox.append((int(bbox_[0]), int(bbox_[1])))
            bbox.append((int(bbox_[2]), int(bbox_[3])))
            bbox.append((int(bbox_[4]), int(bbox_[5])))
            bbox.append((int(bbox_[6]), int(bbox_[7])))

            # 可视化
    #         cv2.putText(final_image_copy, bbox_[-1], (int(bbox_[0]), int(bbox_[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #                     (255, 0, 0), 2)
    #         cv2.line(final_image_copy, bbox[0], bbox[1], (0, 0, 255), 1, 4)
    #         cv2.line(final_image_copy, bbox[1], bbox[2], (0, 0, 255), 1, 4)
    #         cv2.line(final_image_copy, bbox[2], bbox[3], (0, 0, 255), 1, 4)
    #         cv2.line(final_image_copy, bbox[3], bbox[0], (0, 0, 255), 1, 4)
    #
    # cv2.imshow('new_img_bbox', final_image_copy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 处理超出图像边缘的检测框
    new_boxes = merge_bboxes(box_datas, cutx, cuty)

    # 复制一份合并后的图像
    modify_image_copy = new_image.copy()

    # 绘制修正后的检测框
    for boxes in new_boxes:
        # 遍历每张图像中的所有检测框
        # 遍历该张图像中的所有检测框
        for box in boxes:
            bbox_ = box
            bbox = []
            bbox.append((int(bbox_[0]), int(bbox_[1])))
            bbox.append((int(bbox_[2]), int(bbox_[3])))
            bbox.append((int(bbox_[4]), int(bbox_[5])))
            bbox.append((int(bbox_[6]), int(bbox_[7])))

            # 可视化
    #         cv2.putText(modify_image_copy, bbox_[-1], (int(bbox_[0]), int(bbox_[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #                     (255, 0, 0), 2)
    #         cv2.line(modify_image_copy, bbox[0], bbox[1], (0, 0, 255), 1, 4)
    #         cv2.line(modify_image_copy, bbox[1], bbox[2], (0, 0, 255), 1, 4)
    #         cv2.line(modify_image_copy, bbox[2], bbox[3], (0, 0, 255), 1, 4)
    #         cv2.line(modify_image_copy, bbox[3], bbox[0], (0, 0, 255), 1, 4)
    # cv2.imshow('new_img_bbox', modify_image_copy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return new_image,new_boxes


# 主函数，获取图片路径和检测框路径
if __name__ == '__main__':

    # 给出图片文件夹和检测框文件夹所在的位置
    image_dir = 'D:\Remote_Sensor_dataset\\train\crop\\'
    annotation_dir = 'D:\Remote_Sensor_dataset\\train\crop_label/'
    # 图片和标签列表获取
    images_ = [path for path in os.listdir(image_dir)]
    boxes_ = [path for path in os.listdir(annotation_dir)]
    # 单个图片拼接次数
    time = 1
    # 生成后新图片的名称（索引）
    image_num = 0
    for epoch in range(0,time):
        # 顺序遍历图像，随机取其他三张图片进行组合
        for i, img in enumerate(images_):
            # 将主图片(i)从图像列表中移除
            temnporal_img_list = images_[:i] + images_[i + 1:]
            # 随机取三个组合
            select_list = random.sample(range(0, len(images_)), 3)
            # 读取主图与标签
            selected_images = [cv2.imread(image_dir + '\\' + img)]
            selected_boxes = [load_boxes(annotation_dir + '\\' + boxes_[i])]
            # 列表拼接其余三张图片和标签
            for ind in select_list:
                selected_images.append(cv2.imread(image_dir + '\\' + images_[ind]))
            for ind in select_list:
                selected_boxes.append(load_boxes(annotation_dir + '\\' + boxes_[ind]))
            # 存放每张图像和该图像对应的检测框坐标信息
            image_list = []
            for img, box in zip(selected_images, selected_boxes):
                image_list.append([img, box])
            # 缩放、拼接图片
            image, label_list = get_random_data(image_list, input_shape=[416, 416])
            # 剔除超出边界的检测框后的列表
            ann_list = []
            # 最终用于输出到txt的列表
            final_label_list = []
            for label_each in label_list:
                if len(label_each) != 0:
                    ann_list.append(label_each)
            # one label
            if len(ann_list) == 1 and len(ann_list) == 0:
                ann = [str(item) for item in ann_list]
            # multi label
            else:
                for label in ann_list:
                    ann = [str(item) for item in label[0]]
                    ann.append("1")
                    final_label_list.append(' '.join(ann))
            #若图片中无标签，则不生成标签和图片文件
            if len(final_label_list) != 0:
                with open(f"D:\Remote_Sensor_dataset\\train\m_l\\" + str(image_num) + '.txt', 'w') as f:
                    f.write('\n'.join(final_label_list))

                # 保存图片
                cv2.imwrite("D:\Remote_Sensor_dataset\\train\m\\" + str(image_num) + '.tif', image)

                image_num+=1
            else:
                print('nolabel')
