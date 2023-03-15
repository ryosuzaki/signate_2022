import cv2
#import tensorflow as tf
#from tensorflow import keras
import torch
import torchvision
from torchvision import datasets, models, transforms
from ultralytics import YOLO
from PIL import Image
import numpy as np
import os
#import subprocess

class ScoringService(object):
    @classmethod
    def get_model(cls, model_path):
        """Get model method

        Args:
            model_path (str): Path to the trained model directory.

        Returns:
            bool: The return value. True for success.
        """
        
        
        cls.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        #print(device)

        anomaly_models={}
        for category in ["line","sign","light"]:
            anomaly_models[category] = torch.load(os.path.join(model_path,f"{category}.pth")).to(cls.device)
    
        """
        anomaly_models={}
        for category in ["line","sign","light"]:
            anomaly_models[category] = keras.models.load_model(os.path.join(model_path,f"{category}_best.h5"))
        """
        cls.anomaly_models=anomaly_models

        cls.softmax = torch.nn.Softmax(dim=1)
        cls.data_transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        cls.yolo_model=YOLO(os.path.join(model_path,"best.pt"))
        
        return True


    @classmethod
    def predict(cls, input):
        """Predict method

        Args:
            input: Data of the sample you want to make inference from (str)

        Returns:
            list: Inference for the given input.

        """
        prediction = []
        cap = cv2.VideoCapture(input)
        frame_id = 0
        anomaly_label=['その他', '補修不要', '要補修']
        yolo_label=["line","sign","light"]

        while True:
            ret, frame = cap.read()
            if ret:
                category_bool={n:0 for n in ["line","sign","light"]}
                im=Image.fromarray(frame)
                results=cls.yolo_model(source=im)
                for result in results[0].boxes:
                    box=result.xyxy.tolist()[0]
                    #conf=float(result.conf)
                    cls_name=yolo_label[int(result.cls)]
                    #print(box,conf,cls_name)
                    #if (conf>0.2) and (category_bool[cls_name]==0):
                    if (category_bool[cls_name]==0):
                        crop_img=im.crop((box[0],box[1],box[2],box[3])).resize((224, 224))
                        crop_img=cls.data_transform(crop_img)
                        #pred=cls.anomaly_models[cls_name].predict(crop_img)
                        pred=cls.anomaly_models[cls_name](crop_img.unsqueeze(dim=0).to(cls.device))
                        pred=cls.softmax(pred)
                        pred_label=anomaly_label[torch.argmax(pred)]
                        #print(pred_label,pred)
                        category_bool[cls_name]=1 if (pred_label=='要補修')and bool(pred[0][2]>0.8) else 0
                #print(category_bool)
                prediction.append({'frame_id':frame_id, 'line': category_bool["line"], 'sign': category_bool["sign"], 'light': category_bool["light"]})
                
                frame_id += 1
            else:
                break
        
        
        

        return prediction