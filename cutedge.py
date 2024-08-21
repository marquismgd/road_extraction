import cv2 as cv
# 将图像转为灰度图像
from PIL import Image
from postprocess import *
import os
import numpy as np
inputpath=r"D:/unet/skeleton"
outputpath=r"D:/unet/cutedge"

cutedge(inputpath,outputpath)