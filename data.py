import os.path

import torch

from utils import *
from torch.utils.data import Dataset
import os
from PIL import Image
from torchvision import transforms
transform=transforms.Compose([
    transforms.ToTensor()
])

from torchvision.utils import save_image

class MyDataset(Dataset):
    def __init__(self,path):
        self.path=path
        self.name=os.listdir(os.path.join(path,'labels_fcn_sec'))

    def __len__(self):
        return len(self.name)

    def __getitem__(self, index):
        label_name=self.name[index]
        label_path=os.path.join(self.path,'labels_fcn_sec',label_name)
        image_path=os.path.join(self.path,'images',label_name)
        label_image=keep_image_size_open(label_path)
        image=keep_image_size_open_rgb(image_path)
        return transform(image),transform(label_image)

if __name__ =='__main__':
    data=MyDataset(r'F:\Columbus\mosaic\gis\small_dataset')
    print(data[0][0].shape)
    save_image(data[0][1],'test.tif')




