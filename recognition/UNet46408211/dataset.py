import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import torchvision
import torch
import time
import os
import PIL.Image as Image
import PIL
from torch.utils.data import Dataset, DataLoader

# image_dir = '../data/ISIC-2017_Training_Data'
# mask_dir = '../data/ISIC-2017_Training_Part1_GroundTruth'

#----------------------------------------------------------------------
# set the device to cuda if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if not torch.cuda.is_available():
    print('No GPU detected. Using CPU instead.')
print('Using device:', device)
#----------------------------------------------------------------------

class ISICDataset(Dataset):
    
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        # image list should be all .jpg images in the image_dir, NOT .png
        self.images = [img for img in os.listdir(self.image_dir) if img.endswith('.jpg')]
        # self.image_list = os.listdir(self.image_dir)
        # self.image_list = [os.path.join(self.image_dir, i) for i in self.image_list if i.endswith('.jpg')]

    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, index):
        image_path = os.path.join(self.image_dir, self.images[index])
        mask_path = os.path.join(self.mask_dir, self.images[index][:-4] + '_segmentation.png')
        image = np.array(Image.open(image_path).convert('RGB'))
        mask = np.array(Image.open(mask_path).convert('L'), dtype=np.float32)
        mask[mask == 255.0] = 1.0 # convert all 255 values to 1.0 to make it a binary mask
        
        # if self.transform is not None:    # IMPLEMENT TRANSFORMS HERE
        #     image = self.transform(image)
        #     mask = self.transform(mask)
        
        return image, mask