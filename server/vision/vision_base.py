import os
from pathlib import Path
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Rotate, Zoom
from fastai.vision.learner import vision_learner, Resize, cnn_learner
from fastai.vision.models import resnet34
from fastai.metrics import accuracy



def load_data_learner():
    data_dir='data/car_data/car_data'
    train_dir = "data/car_data/car_data/train/*/*.jpg"
    data_path = Path(data_dir)
    batch_size = 64
    data = ImageDataLoaders.from_folder (data_path, train='train', valid_pct = 0.1, bs = batch_size, item_tfms=Resize(224))
    return data, vision_learner(data, resnet34, pretrained = True, metrics = accuracy)

def fit_model(data, learner, epochs, out_dir):
    learner.fit(epochs)
    learner.save(out_dir)

# TODO: shouldn't require data
def load_model(data, path):
    model = vision_learner(data, resnet34, metrics= accuracy)
    model.load(path)
    return model

def predict(model, image_file):
    return model.predict(image_file)[0]
    


    









