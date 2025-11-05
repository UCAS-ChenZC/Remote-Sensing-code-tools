from xml.etree import ElementTree as ET
import os


items = 'A_car,B_car,C_car'


items = [item.strip() for item in items.split(',')]
convert_options = {}

for item in items:
    convert_options[item] = item


def convert_XML_to_DOTA(filename):
    mydoc = ET.parse(filename)
    root = mydoc.getroot()

    objects = root.find('objects')
    items = objects.findall('object')
    output_file = os.path.splitext(os.path.split(filename)[-1])[0] + '.txt'
    with open(f'/home/solid/CD/ciomp/吉林农大-20241116/output/154txt/{output_file}', 'w') as f:   # txt
        ann_list = []
        for item in items:
            label = item.find('possibleresult')
            points = item.find('points')
            label=label.find('name').text
            mapped_label = convert_options[label] if label in convert_options.keys() else convert_options[label.lower()]
            if mapped_label != 'ignore':
                points = [[int(float(item)) for item in point.text.split(',')] for point in points.findall('point')]
                x1, y1 = points[0]
                x2, y2 = points[1]
                x3, y3 = points[2]
                x4, y4 = points[3]
                ann = [x1, y1, x2, y2, x3, y3, x4, y4, mapped_label, 1]
                ann = [str(item) for item in ann]
                ann_list.append(' '.join(ann))
                print (label, mapped_label, x1, y1, x2, y2, x3, y3, x4, y4)

        f.write('\n'.join(ann_list))

if __name__ ==  '__main__':
    xml_files = os.listdir('/home/solid/CD/ciomp/吉林农大-20241116/output/output154') # xml
    os.makedirs('/home/solid/CD/ciomp/吉林农大-20241116/output/154txt', exist_ok=True)    # txt
    for file in xml_files:
        convert_XML_to_DOTA(os.path.join('/home/solid/CD/ciomp/吉林农大-20241116/output/output154', file))    # xml
