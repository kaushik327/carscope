import os
from pathlib import Path
from fastai.vision.data import ImageDataLoaders
from fastai.vision.augment import Rotate, Zoom
from fastai.vision.learner import vision_learner, Resize, cnn_learner
from fastai.vision.models import resnet34
from fastai.metrics import accuracy
from fastai.vision.all import *



def load_data_learner(architecture):
    data_dir='data/car_data/car_data'
    data_path = Path(data_dir)
    batch_size = 64
    data = ImageDataLoaders.from_folder(data_path, train='train', valid_pct = 0.1, bs = batch_size, item_tfms=Resize(224))
    return data, vision_learner(data, architecture, pretrained = True, metrics = accuracy)

def fit_model(learner, epochs, out_file):
    learner.fit(epochs)
    learner.export(f'server/models/{out_file}_{epochs}.pkl')


def load_model(path, device = 'cpu'):
    return load_learner(path, cpu= (device == 'cpu'))

def predict(model, image_file):
    return model.predict(image_file)[0]

if __name__ == '__main__':
    data, learner = load_data_learner(resnet34)
    fit_model(learner, 10, 'data/car_data/car_data/models/resnet34_fine_tuned1')
    
    


    









