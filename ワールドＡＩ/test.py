# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:30:48 2023

@author: n1201023
"""

from tensorflow import keras
from PIL import Image
import numpy as np
import torch
import torchvision
from torchvision import datasets, models, transforms

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

model=torch.load(f"sign_2.pth")
model = model.to(device)
im=Image.open("crop_scene_00_0_1.jpg")
data_transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
im=data_transform(im)

pred=model(im.unsqueeze(dim=0).to(device))
m = torch.nn.Softmax(dim=1)
pred=m(pred)
"""
anomaly_model= keras.models.load_model(f"model_道路標識_best.h5")
anomaly_label=['その他', '補修不要', '要補修']
im=Image.open("crop_scene_00_0_0.jpg")
im=np.array(im)
im=np.array([im])
pred=anomaly_model.predict(im)
pred_label=anomaly_label[np.argmax(pred)]
"""
#pred=anomaly_model.predict("crop_scene_不要.jpg")