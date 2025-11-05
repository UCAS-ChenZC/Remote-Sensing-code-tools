from xml.etree import ElementTree as ET
import os
# code form liu_yd

# items = 'Dump Truck,Van,Small Car,Cargo Truck,other-vehicle,Bus,Trailer,Truck Tractor,Excavator,Tractor'


# items = [item.strip() for item in items.split(',')]
convert_options = {}

# for item in items:
#     convert_options[item] = item


def convert_XML_to_DOTA(filename):
    mydoc = ET.parse(filename)
    root = mydoc.getroot()

    #objects = root.find('object')
    items = objects.findall('object')
    output_file = os.path.splitext(os.path.split(filename)[-1])[0] + '.txt'
    with open(f'/media/solid/T9/333/txt/{output_file}', 'w') as f:   # txt
        ann_list = []
        for item in items:
            label = item.find('possibleresult')
            points = item.find('points')
            label=label.find('name').text
            # mapped_label = convert_options[label] if label in convert_options.keys() else convert_options[label.lower()]
            # mapped_label = convert_options[label]
            mapped_label = label
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
    xml_files = os.listdir('/media/solid/T9/333/label') # xml
    os.makedirs('/media/solid/T9/333/txt', exist_ok=True)    # txt
    for file in xml_files:
        convert_XML_to_DOTA(os.path.join('/media/solid/T9/333/label', file))    # xml
