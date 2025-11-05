import os
import shutil, os
########################################################################################################################
# 筛选具有特定类别的标签以及图片，并另存为（DOTA类型的txt文件）
########################################################################################################################

path = "I:\\train\labelTxt-v1.5\DOTA-v1.5_train" #文件夹目录
image_path = "I:\\train\images\\total"#图片目录
files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file in files:
    f = open(path + "/" + file);
    iter_f = iter(f);  # 创建迭代器
    str = ""
    flag = False
    for line in iter_f:  # 遍历文件，一行行遍历，读取文本
        if line.find("small-vehicle")!= -1 :
            flag = True
        if line.find("large-vehicle") != -1:
            flag = True

    if flag:
        shutil.copy(path + "/" + file,"I:\CleanComplete\label")#标签保存目录
        image_file = image_path + "/" + file[:-4] + '.png'
        shutil.copy(image_file,"I:\CleanComplete\image")#图像保存目录


########################################################################################################################
# 替换标签中的x类别名为y类别名（DOTA类型的txt文件）
########################################################################################################################
import os
import shutil, os
path = "I:\CleanComplete\label_row" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file in files:
    f = open(path + "/" + file);
    iter_f = iter(f);  # 创建迭代器
    str = ""
    flag = False
    newName = 'I:\CleanComplete\label\\' + file # 新标签保存路径

    for index,line in enumerate(iter_f):  # 遍历文件，一行行遍历，读取文本
        if index==0 or index==1:
            with open(newName, "a") as f:
                f.write(line)
        else:
            if line.find("small-vehicle")!= -1 :
                with open(newName, "a") as f:
                    f.write(line.replace("small-vehicle","Small_Car"))
            if line.find("large-vehicle") != -1:
                with open(newName, "a") as f:
                    f.write(line.replace("large-vehicle","Cargo_Truck"))
########################################################################################################################
# 批量删除标签文件中除某些类别外的所有标签（Fair1M类型的xml文件）
########################################################################################################################
#读取xml
import os
import shutil, os
import xml.etree.ElementTree as ET

# 筛选
path = "J:\TenCar\\validation\labelXmls" #文件夹目录
image_path = "D:\Remote_Sensor_dataset\\validation\images"#图片目录
files= os.listdir(path) #得到文件夹下的所有文件名称
s = []
for file in files:

    tree = ET.parse(path + "/" + file)

    root = tree.getroot()

    str = ""
    flag = False
    otherFlag = False
    inflag = False
    #创建新的xml
    newroot = ET.Element('data')

    indexlist = []
    for z in root.find('objects'):
        if z.find('possibleresult').find('name').text == 'Bus':
            flag = True
            object_flag = True
        elif z.find('possibleresult').find('name').text == 'Trailer':
            flag = True
            object_flag = False
        elif z.find('possibleresult').find('name').text == 'Tractor':
            flag = True
            object_flag = True
        elif z.find('possibleresult').find('name').text == 'Excavator':
            flag = True
            object_flag = True
        elif z.find('possibleresult').find('name').text == 'Truck Tractor':
            flag = True
            object_flag = True
        # another five car class
        elif z.find('possibleresult').find('name').text == 'other-vehicle':
            flag = True
            object_flag = True
        elif z.find('possibleresult').find('name').text == 'Small Car':
            flag = True
            object_flag = True
        elif z.find('possibleresult').find('name').text == 'Cargo Truck':
            flag = True
            object_flag = True
        elif z.find('possibleresult').find('name').text == 'Dump Truck':
            flag = True
            object_flag = True
        elif z.find('possibleresult').find('name').text == 'Van':
            flag = True
            object_flag = True
        else:
            print(z.find('possibleresult').find('name').text)

            indexlist.append(z)
    for child in indexlist:
        root.find('objects').remove(child)
    newroot = root
    tree = ET.ElementTree(newroot)
    tree.write("J:\TenCar\\validation\label_clean\\" + file) # 新标签保存路径