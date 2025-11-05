import aug

A=aug.aug("/home/solid/TZ/Datasets/Space_Based_v10/111","/home/solid/TZ/Datasets/Space_Based_v10/222","/home/solid/TZ/Datasets/Space_Based_v10/333","/home/solid/TZ/Datasets/Space_Based_v10/444")# 原始图片路径 原始lables路径 扩充到的图片路径 扩充到的lables路径
A.Rotate(angle=30)

# A.RandomResize()
#A.AddWeather()
