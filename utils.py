from PIL import Image
import os
import numpy as np

def keep_image_size_open(path, size=(1024, 1024)):
    img = Image.open(path)
    temp = max(img.size)
    mask = Image.new('P', (temp, temp))
    mask.paste(img, (0, 0))
    mask = mask.resize(size)
    return mask


def keep_image_size_open_rgb(path, size=(1024, 1024)):
    img = Image.open(path)
    temp = max(img.size)
    mask = Image.new('RGBA', (temp, temp))
    mask.paste(img, (0, 0))
    mask = mask.resize(size)
    return mask

# 创建文件夹函数
def mkdir(path):
    # os.path.exists 函数判断文件夹是否存在
    folder = os.path.exists(path)

    # 判断是否存在文件夹如果不存在则创建为文件夹
    if not folder:
        # os.makedirs 传入一个path路径，生成一个递归的文件夹；如果文件夹存在，就会报错,因此创建文件夹之前，需要使用os.path.exists(path)函数判断文件夹是否存在；
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print('文件夹创建成功：', path)

    else:
        print('文件夹已经存在：', path)

def gettiflist(path):
    folder=os.path.exists(path)

    if not folder:
        print("文件夹路径不存在")

    else:
        file_name_list=[]
        for file in os.listdir(path):
            if file.endswith(".tif"):
                file_name_list.append(file)

    return file_name_list



def binarize_image(image_path, output_path, threshold):
    """
    Binarize a grayscale image and save the binary image.

    Parameters:
    - image_path: str, path to the input image.
    - output_path: str, path to save the output binary image.
    - threshold: int, threshold for binarization.
    """

    # 打开图像
    image = Image.open(image_path)

    # 转换为灰度图像（如果它不是灰度的）
    image = image.convert("L")

    # 转换为NumPy数组
    image_np = np.array(image)

    # 应用阈值进行二值化
    binary_image_np = (image_np > threshold).astype(np.uint8)

    # 转换回PIL图像
    binary_image = Image.fromarray(binary_image_np, "L")

    # 保存二值化后的图像
    binary_image.save(output_path)

# 使用函数进行二值化
#binarize_image("path/to/your/image.jpg", "binary_image.png", threshold=128)
if __name__ == '__main__':
    input_path=r"F:\Columbus_paper\image_testfcnsec"
    output_path=r"F:\Columbus_paper\image_fcntestsec_binary"
    input_tif_list=gettiflist(input_path)
    for img in input_tif_list:
        img_in=os.path.join(input_path,img)
        img_out = os.path.join(output_path, img)
        binarize_image(img_in,img_out,35)



