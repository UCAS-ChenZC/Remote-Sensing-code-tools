from PIL import Image

def resize_image(input_path, output_path, target_size=(200, 300)):
    """
    将 JPG 图片压缩为指定大小
    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param target_size: (宽, 高)，如 (200, 300)
    """
    with Image.open(input_path) as img:
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
        resized_img.save(output_path, format='JPEG')
        print(f"图片已保存至: {output_path}")

# 示例
resize_image("/home/solid/下载/个人/350821200003290413.jpg", "/home/solid/下载/350821200003290413.jpg")


