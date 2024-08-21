import os
from PIL import Image
import numpy as np

# 指定目录路径
imagepath = r'F:\Columbus_paper\images'
osmpath=r"F:\Columbus_paper\labels"
firstpath =r"F:\Columbus_paper\images_test_binary"
secondpath =r"F:\Columbus_paper\images_testsec_binary"
# 获取目录下的所有文件名
secondfiles = os.listdir(secondpath)
#定义函数
def convert_to_rgb(image_path):
    # 读取图像
    gray_image = Image.open(image_path)
    # 转换为numpy数组并乘以255
    np_image = np.array(gray_image) * 255
    # 确保数值为uint8类型
    np_image = np_image.astype(np.uint8)
    # 将处理后的图像转换为RGB
    rgb_image = Image.fromarray(np_image).convert('RGB')
    return rgb_image


def combine_and_resize(binary_image1_path, binary_image2_path, rgba_image_path,binary_image3_path):
    # 读取图像
    #binary_image1 = Image.open(binary_image1_path).convert('L')
    binary_image1 = convert_to_rgb(binary_image1_path)
    #binary_image2 = Image.open(binary_image2_path).convert('L')
    binary_image2 = convert_to_rgb(binary_image2_path)
    binary_image3 = convert_to_rgb(binary_image3_path)
    rgba_image = Image.open(rgba_image_path)

    # 转换二值图像为RGB
    #binary_image1 = binary_image1.convert('RGB')
    #binary_image2 = binary_image2.convert('RGB')

    # 确定新图像的尺寸
    total_width = binary_image1.width + binary_image2.width + rgba_image.width + binary_image3.width
    max_height = max(binary_image1.height, binary_image2.height, rgba_image.height,binary_image3.height)

    # 创建新图像
    new_image = Image.new('RGB', (total_width, max_height))

    # 合并图像
    new_image.paste(rgba_image, (0, 0))
    new_image.paste(binary_image3.convert('RGB'), (rgba_image.width, 0))
    new_image.paste(binary_image1.convert('RGB'), (rgba_image.width + binary_image3.width, 0))
    new_image.paste(binary_image2.convert('RGB'), (binary_image1.width + rgba_image.width + binary_image3.width, 0))

    # 重采样图像至原大小的一半
    new_size = (new_image.width // 2, new_image.height // 2)
    resized_image = new_image.resize(new_size, Image.ANTIALIAS)

    return resized_image

#使用函数
save_path=r"F:\Columbus_paper\concat"
for file in secondfiles:
    imgfile=os.path.join(imagepath,file)
    firstfile=os.path.join(firstpath,file)
    secondfile=os.path.join(secondpath,file)
    osmfile=os.path.join(osmpath,file)
    concat=combine_and_resize(firstfile,secondfile,imgfile,osmfile)
    concat.save(os.path.join(save_path,file))


