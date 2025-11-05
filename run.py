# -*- codeing: utf-8 -*- #
"""
# @file             main_docker.py
# @brief            一个尝试用于docker的脚本文件
# @note
# @version          V1.00
# @date             2024/7/2 下午4:32
# @author           Atenolol
# @copyright        CIOMP
"""

from datetime import datetime
from mmdet.apis import inference_detector
from mmdet.apis import init_detector
from mmdet.apis import show_result_pyplot

# import sys
# sys.path.append('/home/solid/TZ/LSKNet/workspace/LSKNet')

import numpy as np
import cv2 as cv
import mmrotate

import os
from tqdm import tqdm
import xml.etree.ElementTree as ElementTree
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input_path', help='Image file')
    parser.add_argument('output_path', help='Config file')
    args = parser.parse_args()
    return args


def pretty_xml(element, indent, newline, level=0):
    if element:
        if (element.text is None) or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    temp = list(element)
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else:
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)


def output_results_from_images(config_path, checkpoint_path, path_in, path_ou):
    # # FAIR V1
    # classes = ('Boeing737', 'Boeing777', 'Boeing747', 'Boeing787', 'A321', 'A220', 'A330', 'A350', 'C919', 'ARJ21',
    #            'other-airplane', 'Passenger_Ship', 'Motorboat', 'Fishing_Boat', 'Tugboat', 'Engineering_Ship',
    #            'Liquid_Cargo_Ship', 'Dry_Cargo_Ship', 'Warship', 'other-ship', 'Small_Car', 'Bus', 'Cargo_Truck',
    #            'Dump_Truck', 'Van', 'Trailer', 'Tractor', 'Truck_Tractor', 'Excavator', 'other-vehicle',
    #            'Baseball_Field', 'Basketball_Court', 'Football_Field', 'Tennis_Court', 'Roundabout', 'Intersection',
    #            'Bridge')
    # DOTA V1
    # classes = ('plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship',
    #            'tennis-court', 'basketball-court', 'storage-tank', 'soccer-ball-field', 'roundabout', 'harbor',
    #            'swimming-pool', 'helicopter')
    # 魏希来
    # classes = ('Dump Truck', 'Van', 'Small Car', 'Cargo Truck', 'other-vehicle', 'Bus', 'Trailer', 'Truck Tractor',
    #           'Excavator', 'Tractor')
    # 张德浩
    # classes = ('Small Car', 'Bus', 'Cargo Truck', 'Dump Truck', 'Van', 'Trailer', 'Tractor', 'Excavator',
    #            'Truck Tractor', 'other-vehicle')


    classes = ('Dump Truck', 'Van', 'Small Car', 'Cargo Truck', 'other-vehicle', 'Bus', 'Trailer', 'Truck Tractor', 'Excavator', 'Tractor')

    today = datetime.now().strftime('%Y-%m-%d')
    model = init_detector(config=config_path, checkpoint=checkpoint_path, device='cuda:0')
    print(checkpoint_path, config_path)
    img_files = [p for p in os.listdir(path_in) if p.endswith(".tif")]
    for img_file in tqdm(img_files):
        image = cv.imread(os.path.join(path_in, img_file))
        if image is None:
            continue
        result = inference_detector(model, os.path.join(path_in, img_file))
        if result is None:
            continue
        annotation = ElementTree.Element("annotation")

        source = ElementTree.SubElement(annotation, "source")
        ElementTree.SubElement(source, "filename").text = img_file
        ElementTree.SubElement(source, "origin").text = "Optical"
        research = ElementTree.SubElement(annotation, "research")
        ElementTree.SubElement(research, "version").text = "1.0"
        ElementTree.SubElement(research, "author").text = "Cyber"
        ElementTree.SubElement(research, "pluginclass").text = "object detection"
        ElementTree.SubElement(research, "time").text = str(today)

        size = ElementTree.SubElement(annotation, "size")
        ElementTree.SubElement(size, "height").text = str(image.shape[0])
        ElementTree.SubElement(size, "width").text = str(image.shape[1])
        ElementTree.SubElement(size, "depth").text = str(3)
        ElementTree.SubElement(annotation, "objects")

        bboxes = np.vstack(result)
        labels = [np.full(bbox.shape[0], i, dtype=np.int32) for i, bbox in enumerate(result)]
        labels = np.concatenate(labels)
        score_thr = 0.6
        if score_thr > 0.0:
            scores = bboxes[:, -1]
            finds = scores > score_thr
            bboxes = bboxes[finds, :]
            labels = labels[finds]
        for i in range(bboxes.shape[0]):
            xc, yc, w, h, ag = bboxes[i][:5]
            wx, wy = w / 2 * np.cos(ag), w / 2 * np.sin(ag)
            hx, hy = -h / 2 * np.sin(ag), h / 2 * np.cos(ag)
            p1 = (int(round(xc - wx - hx)), int(round(yc - wy - hy)))
            p2 = (int(round(xc + wx - hx)), int(round(yc + wy - hy)))
            p3 = (int(round(xc + wx + hx)), int(round(yc + wy + hy)))
            p4 = (int(round(xc - wx + hx)), int(round(yc - wy + hy)))
            objs = annotation.find("objects")
            obj = ElementTree.SubElement(objs, "object")
            ElementTree.SubElement(obj, "coordinate").text = "pixel"
            ElementTree.SubElement(obj, "type").text = "rectangle"
            ElementTree.SubElement(obj, "description").text = "None"
            possible_result = ElementTree.SubElement(obj, "possibleresult")
            ElementTree.SubElement(possible_result, "name").text = str(classes[labels[i]])
            ElementTree.SubElement(possible_result, "probability").text = str(bboxes[i][-1])
            points = ElementTree.SubElement(obj, "points")
            ElementTree.SubElement(points, "point").text = "{:.6f},{:.6f}".format(xc - wx - hx, yc - wy - hy)
            ElementTree.SubElement(points, "point").text = "{:.6f},{:.6f}".format(xc + wx - hx, yc + wy - hy)
            ElementTree.SubElement(points, "point").text = "{:.6f},{:.6f}".format(xc + wx + hx, yc + wy + hy)
            ElementTree.SubElement(points, "point").text = "{:.6f},{:.6f}".format(xc - wx + hx, yc - wy + hy)
            ElementTree.SubElement(points, "point").text = "{:.6f},{:.6f}".format(xc - wx - hx, yc - wy - hy)
        pretty_xml(annotation, '\t', '\n')
        tree = ElementTree.ElementTree(annotation)
        tree.write(os.path.join(path_ou, "{}.xml".format(img_file[:-4])), xml_declaration=True, encoding="utf-8")


def main():
    args = parse_args()
    output_results_from_images("/workspace/LSKNet/configs/spacebasenet/lsk_s_fpn_1x_spacebase_le90.py",
                               "/model_path/epoch_12.pth",
                               args.input_path,
                               args.output_path)


if __name__ == '__main__':
    main()
