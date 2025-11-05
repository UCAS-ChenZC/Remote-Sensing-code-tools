## 从算法检测的结果（Line 23 result），转成xml格式（科目二格式，可能需要改）
"""python run.py /input_path /output_path"""
import sys
import os
import os.path as osp
from datetime import datetime
import glob
import xml.etree.ElementTree as ET

from PIL import Image
import torch
from tqdm import tqdm
from mmcv.transforms import Compose

from mmdet.apis import init_detector, inference_detector
from mmdet.structures.bbox import HorizontalBoxes
from mmdet.utils import register_all_modules
from mmdet.utils.misc import get_test_pipeline_cfg
from mmrotate.utils import register_all_modules
from mmrotate.structures.bbox import RotatedBoxes

device = 'cuda:0'
today = datetime.now().strftime('%Y-%m-%d')


def det_vis(cfg_filename, ckpt_filename, in_path, out_path):
    classes = ['Boeing737', 'Boeing777', 'Boeing747', 'Boeing787', 'A321', 'A220', 'A330', 'A350', 'C919', 'ARJ21', 'other-airplane']

    # register all modules in mmrotate into the registries
    register_all_modules()

    # build the model from a config file and a checkpoint file
    model = init_detector(
        cfg_filename, ckpt_filename, palette='dota', device=device)
    model.eval()

    img_folder = in_path
    img_files = glob.glob(os.path.join(img_folder, "*.tif"))

    for img_file in tqdm(img_files):
        _, fname = os.path.split(img_file)
        img_name = fname[:-4]
        if int(img_name) > 750:  # FIXME(HQSun): 
            continue

        result = inference_detector(model, img_file,
                                    Compose(get_test_pipeline_cfg(model.cfg)))

        # add save result
        if result is not None:
            # annotation = ET.Element("annotation")
            #
            # source = ET.SubElement(annotation, "source")
            # ET.SubElement(source, "filename").text = img_name + ".tif"
            # ET.SubElement(source, "origin").text = "Optical"
            #
            # research = ET.SubElement(annotation, "research")
            # ET.SubElement(research, "version").text = "1.0"
            # ET.SubElement(research, "author").text = "Cyber"
            # ET.SubElement(research, "pluginclass").text = "object detection"
            # ET.SubElement(research, "time").text = str(today)
            #
            # size = ET.SubElement(annotation, "size")
            img = Image.open(img_file)
            # ET.SubElement(size, "height").text = str(img.height)
            # ET.SubElement(size, "width").text = str(img.width)
            # ET.SubElement(size, "depth").text = str(3)
            #
            # ET.SubElement(annotation, "objects")

            if 'pred_instances' in result:
                pred_instances = result.pred_instances
                # pred_instances = pred_instances[pred_instances.scores.float() > args.score_thr]  ######

                if 'bboxes' in pred_instances:
                    bboxes = pred_instances.bboxes
                    labels = pred_instances.labels
                    scores = pred_instances.scores
                    labels = [label for label in labels]
                    scores = [score for score in scores]

                    bboxes = RotatedBoxes(bboxes)
                    bboxes = bboxes.cpu()

                    polygons = bboxes.convert_to('qbox').tensor
                    polygons = polygons.reshape(-1, 4, 2)
                    polygons = [p for p in polygons]

                    for i, _ in enumerate(labels):
                        objs = annotation.find("objects")
                        obj = ET.SubElement(objs, "object")

                        ET.SubElement(obj, "coordinate").text = "pixel"
                        ET.SubElement(obj, "type").text = "rectangle"
                        ET.SubElement(obj, "description").text = "None"
                        possibleresult = ET.SubElement(obj, "possibleresult")
                        ET.SubElement(possibleresult, "name").text = str(classes[labels[i].item()])
                        ET.SubElement(possibleresult, "probability").text = str(scores[i].item())  ####
                        points = ET.SubElement(obj, "points")
                        ET.SubElement(points, "point").text = "{:.6f},{:.6f}".format(polygons[i][0][0].item(), polygons[i][0][1].item())
                        ET.SubElement(points, "point").text = "{:.6f},{:.6f}".format(polygons[i][1][0].item(), polygons[i][1][1].item())
                        ET.SubElement(points, "point").text = "{:.6f},{:.6f}".format(polygons[i][2][0].item(), polygons[i][2][1].item())
                        ET.SubElement(points, "point").text = "{:.6f},{:.6f}".format(polygons[i][3][0].item(), polygons[i][3][1].item())
                        ET.SubElement(points, "point").text = "{:.6f},{:.6f}".format(polygons[i][0][0].item(), polygons[i][0][1].item())

            tree = ET.ElementTree(annotation)
            tree.write(os.path.join(out_path, "{}.xml".format(img_name)), xml_declaration=True, encoding="utf-8")
