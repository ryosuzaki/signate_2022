# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:30:48 2023

@author: n1201023
"""

from tensorflow import keras
from PIL import Image
import numpy as np




anomaly_model= keras.models.load_model(f"model_道路標識_best.h5")
anomaly_label=['その他', '補修不要', '要補修']
im=Image.open("crop_scene_00_0_0.jpg")
im=np.array(im)
im=np.array([im])
pred=anomaly_model.predict(im)
pred_label=anomaly_label[np.argmax(pred)]
"""
#pred=anomaly_model.predict("crop_scene_不要.jpg")
"""