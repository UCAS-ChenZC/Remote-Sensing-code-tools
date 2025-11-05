import os
import shutil
import labelme
import numpy as np
import PIL.Image
import base64
import io

 
input_folder = "/home/solid/桌面/820To_Yao/处理后/satellite_1"  # 输入文件夹路径，包含多个JSON标记文件
output_folder = "/home/solid/桌面/820To_Yao/处理后/mask"  # 输出文件夹路径，用于保存PNG图像
 


os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        input_path = os.path.join(input_folder, filename)
        output_subfolder = os.path.join(output_folder, os.path.splitext(filename)[0])

        if os.path.exists(output_subfolder):
            shutil.rmtree(output_subfolder)
        os.makedirs(output_subfolder)

        label_file = labelme.LabelFile(filename=input_path)

        # === 关键部分：判断 imageData 是否可用 ===
        if label_file.imageData is not None:
            img = labelme.utils.img_b64_to_arr(label_file.imageData)
        else:
            image_path = os.path.join(os.path.dirname(input_path), label_file.imagePath)
            img = np.asarray(PIL.Image.open(image_path))

        # 标签图与标签名
        lbl, lbl_names = labelme.utils.labelme_shapes_to_label(img.shape, label_file.shapes)

        # 保存原图
        PIL.Image.fromarray(img).save(os.path.join(output_subfolder, "img.png"))

        # 保存标签图
        PIL.Image.fromarray(lbl.astype(np.uint8)).save(os.path.join(output_subfolder, "label.png"))

        # 保存 label name 映射
        with open(os.path.join(output_subfolder, "label_names.txt"), "w") as f:
            for name in lbl_names:
                f.write(name + "\n")

        print(f"✅ Converted: {input_path}")

