from PIL import Image
import numpy as np
import time

def dilation(image, kernel):
    img_height, img_width = image.shape
    k_height, k_width = kernel.shape

    # 计算输出图像的尺寸
    output = np.zeros_like(image)

    # 计算图像和核的起始和终止位置
    pad_height = k_height // 2
    pad_width = k_width // 2

    for i in range(pad_height, img_height - pad_height):
        for j in range(pad_width, img_width - pad_width):
            region = image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1]
            output[i, j] = np.max(region * kernel)

    return output


def erosion(image, kernel):
    img_height, img_width = image.shape
    k_height, k_width = kernel.shape

    # 计算输出图像的尺寸
    output = np.zeros_like(image)

    # 计算图像和核的起始和终止位置
    pad_height = k_height // 2
    pad_width = k_width // 2

    for i in range(pad_height, img_height - pad_height):
        for j in range(pad_width, img_width - pad_width):
            region = image[i - pad_height:i + pad_height + 1, j - pad_width:j + pad_width + 1]
            output[i, j] = np.min(region * kernel)

    return output


#inputpath = r"F:\Columbus_paper\mosaic\images_test_binary_sk.tif"

inputpath = r"F:\Columbus_paper\image_fcntest_binary\1173.tif"
outputpath = r"F:\Columbus_paper\mosaicfcn\mosaicfcnde2.tif"

# 提高像素限制
Image.MAX_IMAGE_PIXELS = 20000000000  # 或其他适当的大数
# 读取图像并转换为灰度模式
image = Image.open(inputpath).convert("L")
image = np.array(image)

# 定义结构元素（kernel）
kernel = np.ones((3, 3), dtype=np.uint8)

# 膨胀
for i in range(10):
    image = dilation(image, kernel)
    print("膨胀一次"+time.asctime(time.localtime(time.time())))
# 腐蚀
for i in range(18):
    image = erosion(image, kernel)
    print("腐蚀一次"+time.asctime(time.localtime(time.time())))


#保存
image=Image.fromarray(image)
image.save(outputpath)
# 转换为 PIL 图像并显示
#Image.fromarray(dilated_image).show()
#Image.fromarray(eroded_image).show()

