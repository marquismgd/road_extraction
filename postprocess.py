# 导入库
#import matplotlib
#import matplotlib.pyplot as plt
import os
import time
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2, 40).__str__()
import cv2 as cv
# 将图像转为灰度图像
from PIL import Image
from utils import *

import numpy as np


# 定义像素点周围的8邻域
#                P9 P2 P3
#                P8 P1 P4
#                P7 P6 P5

def neighbours(x, y, image):
    img = image
    x_1, y_1, x1, y1 = x - 1, y - 1, x + 1, y + 1
    return [img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],  # P2,P3,P4,P5
            img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1]]  # P6,P7,P8,P9


# N(p1)表示与1相邻的8个像素点中，为前景像素点的个数。
def sum_number(n):
    S = 0
    for i in range(len(n)):
        #if (n[i] == 255):
        if (n[i] == 1):
            S += 1
    return S


# 计算邻域像素从0变化到1的次数
def transitions_num(neighbours):
    n = neighbours + neighbours[0:1]
    S = 0
    for i in range(len(n) - 1):
        if ((n[i], n[i + 1]) == (0, 1)):
        #if ((n[i], n[i + 1]) == (0, 255)):
            S += 1
            # print(S)
    return S

##########################################################################
#裁边算法

def cutedge(inputfolder,outputfolder):
    tiflist=gettiflist(inputfolder)
    for tif in tiflist:
        img = cv.imread(os.path.join(inputfolder, tif), 0)
        shape = img.shape
        img_new = img[2:shape[0]-2, 2:shape[1]-2]
        img_new = np.pad(img_new, ((2,2), (2,2)), 'constant',constant_values = (0,0))
        print(os.path.join(tif, outputfolder))
        cv.imwrite(os.path.join(outputfolder,tif), img_new)
        print(tif)

#########################################################################

# Zhang-Suen 细化算法
def zhangSuen(imagefile,outputpath):
    image=cv.imread(imagefile)
    image=cv.cvtColor(image, cv.COLOR_BGRA2GRAY)

    # 创建一个核（或称结构元素）。这里使用一个3x3的矩形核。
    kernel = np.ones((3, 3), np.uint8)

    # 膨胀操作
    image = cv.dilate(image, kernel, iterations=8)
    print("pengzhang")
    # 腐蚀操作
    image = cv.erode(image, kernel, iterations=14)
    print("fushi")
    #ret, image = cv.threshold(image, 0.5, 255, cv.THRESH_BINARY)
    ret, image = cv.threshold(image, 0.5, 1, cv.THRESH_BINARY)
    Image_Thinned = image.copy()  # Making copy to protect original image
    changing1 = changing2 = 1
    while changing1 or changing2:  # Iterates until no further changes occur in the image
        print("loop"+time.asctime(time.localtime(time.time())))
        # Step 1
        changing1 = []
        rows, columns = Image_Thinned.shape
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(x, y, Image_Thinned)
                # print(P2, P3, P4, P5, P6, P7, P8, P9,P2)
                #print(len(n))
                # print(sum_number(n))
                # print(transitions_num(n))
                #if (Image_Thinned[x][y] == 255 and  # Condition 0: Point P1 in the object regions
                if (Image_Thinned[x][y] == 1 and  # Condition 0: Point P1 in the object regions
                        2 <= sum_number(n) <= 6 and  # Condition 1: 2<= N(P1) <= 6
                        transitions_num(n) == 1 and  # Condition 2: S(P1)=1
                        P2 * P4 * P6 == 0 and  # Condition 3
                        P4 * P6 * P8 == 0):  # Condition 4
                    changing1.append((x, y))
        for x, y in changing1:
            Image_Thinned[x][y] = 0
        # Step 2
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2, P3, P4, P5, P6, P7, P8, P9 = n = neighbours(x, y, Image_Thinned)
                #if (Image_Thinned[x][y] == 255 and  # Condition 0
                if (Image_Thinned[x][y] == 1 and  # Condition 0
                        2 <= sum_number(n) <= 6 and  # Condition 1
                        transitions_num(n) == 1 and  # Condition 2
                        P2 * P4 * P8 == 0 and  # Condition 3
                        P2 * P6 * P8 == 0):  # Condition 4
                    changing2.append((x, y))
        for x, y in changing2:
            Image_Thinned[x][y] = 0
    shape = Image_Thinned.shape
    img_new = Image_Thinned[2:shape[0] - 2, 2:shape[1] - 2]
    img_new = np.pad(img_new, ((2, 2), (2, 2)), 'constant', constant_values=(0, 0))
    #tif=imagefile.split("\\")
    #tif=tif[len(tif)-1]
    print(outputpath)
    cv.imwrite(outputpath, img_new)
    #print(tif)
    #cv.imwrite(outputpath,Image_Thinned)
    #return Image_Thinned


if __name__=="__main__":
    inputpath = r"F:\Columbus_paper\mosaicfcn\mosaicfcn.tif"
    outputpath = r"F:\Columbus_paper\mosaicfcn\mosaicfcnde4.tif"


    # Increase the pixel limit
    #cv.CV_IO_MAX_IMAGE_PIXELS = 20000000000


    zhangSuen(inputpath,outputpath)