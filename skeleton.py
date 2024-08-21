from postprocess import *
from utils import *
import cv2 as cv



inputpath = r"F:\Columbus_paper\mosaicfcn\mosaicfcn.tif"
outputpath = r"F:\Columbus_paper\mosaicfcn\mosaicfcnde.tif"


for image in gettiflist(inputpath):
    outputpath = r"F:\Columbus_paper\images_testsec_binary_sk"
    zhangSuen(os.path.join(inputpath,image),os.path.join(outputpath,image))





