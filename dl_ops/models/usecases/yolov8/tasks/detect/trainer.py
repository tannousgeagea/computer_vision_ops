import os
import yaml
import torch
import shutil
import logging
from ultralytics import YOLO
from tqdm import tqdm
from glob import glob

import django
django.setup()
import augmentation.main
from database.models import Models, ModelMetrics, ModelEval, EdgeBoxInfo, Image, Objects, Annotation, DatasetAtTrainTime
import augmentation
from utils.tools import increment_version as increment
from utils.common import out
from utils.data_utils import get_model_path


optimizer = 'SGD'
imgsz = 640
lr0 = 1e-5
lrf = 1e-7
epochs = 100
batch = 8
augment = False
num_workers = 2
save_dir = "/home/appuser/data/results"
workspace_name = "gml-luh"

out = out
src_train_val = os.environ.get('SRC_TRAIN_VAL')

def get_best_model():
    edge_box = EdgeBoxInfo.objects.get(sensor_box_id=os.environ.get('sensor_box_id'))
    model = Models.objects.filter(sensor_box=edge_box)
    best_model = ModelEval.objects.filter(model_id__in=model.values_list('id', flat=True)).order_by('-metric_value').first()
    return Models.objects.get(model_id=best_model.model)

def get_last_model():
    edge_box = EdgeBoxInfo.objects.get(sensor_box_id=os.environ.get('sensor_box_id'))
    return Models.objects.filter(sensor_box=edge_box).order_by('-model_tag').first()
    

def get_data():
    meta_data = Image.objects.filter(annotated=True).filter(mode__in=['train', 'val'])
    pbar = tqdm(meta_data, ncols=125)
    
    if os.path.exists(src_train_val):
        print(f'PATH Exists {src_train_val}. Creating New Path')
        shutil.rmtree(src_train_val)
        
    for image in pbar:
        pbar.set_description('Transferring Data')
        if not os.path.exists(src_train_val + "/" + image.mode + "/images/"):
            os.makedirs(src_train_val + "/" + image.mode + "/images/")
        
        if not os.path.exists(src_train_val + "/" + image.mode + "/labels/"):
            os.makedirs(src_train_val + "/" + image.mode + "/labels/")
            
        shutil.copy(image.image_file.url, src_train_val + "/" + image.mode + "/images/")
        shutil.copy(image.annotation.url, src_train_val + "/" + image.mode + "/labels/")

    objects = Objects.objects.values_list('object_class', flat=True).distinct()
    
    data = {
        'path': src_train_val,
        'train': 'train/images',
        'val': 'val/images',
        'nc': len(objects),
        'names': [Annotation.objects.get(id=item).object_class_name for item in objects]
    }
    
    data_yaml = out + "/data.yaml"
    with open(data_yaml, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

    return data_yaml

def load_model(weights):
    print(f'Loading model {weights}')
    assert os.path.exists(weights), f"Model Weights not Found {weights}"
    return YOLO(weights)

def save_model(last_model):
    TAG = increment(last_model.model_tag)
    out = os.environ.get('OUT', '/media/')
    out = out + '/models/' + last_model.model_name + '/' + TAG
    
    
    print(out)
    if not os.path.exists(out):
        os.makedirs(out)
        
    filename = os.path.basename(increment(last_model.model_file.url))
    m = Models()
    m.model_id = increment(last_model.model_id)
    m.model_name = last_model.model_name
    m.sensor_box = last_model.sensor_box
    m.model_tag = TAG
    m.model_file = get_model_path(m, filename)
    shutil.copyfile(f'./runs/detect/{workspace_name}/weights/best.pt', m.model_file.url)
    for f in glob(f'./runs/detect/{workspace_name}/*.jpg') + glob(f'./runs/detect/{workspace_name}/*.png'):
        shutil.copy(f, out)
        
    m.save()
        
    try:
        shutil.rmtree('./runs')
    except:
        pass
    
    
    return m
    
def save_model_results(model, best_model):
    metrics = model.val()
    
    model_eval = ModelEval()
    model_eval.model = Models.objects.get(model_id=best_model.model_id)
    model_eval.metric = ModelMetrics.objects.get(metric='mean_average_precision')
    model_eval.metric_value = round(metrics.box.map50, 4)
    model_eval.lr = lr0
    model_eval.num_epochs = epochs
    model_eval.optimizer = optimizer
    model_eval.imgsz = imgsz
    model_eval.batch_size = batch
    
    model_eval.save()

def train():
    success = False
    try:
        try:
            shutil.rmtree('./runs')
        except:
            pass
        
        assert optimizer in ['SGD', 'ADAM'], f'Unsupported optimizer. expected one of [SGD, ADAM], got {optimizer}'
        
        best_model = get_best_model()
        model = load_model(best_model.model_file.url)
        assert model is not None, f"Model Is None"
        
        data = get_data()
        assert os.path.exists(data), f'Data Not Found {data}'
        
        augmentation.main.main(mode='by-images')
        
        save_dir
        r = model.train(
            data=data,
            optimizer=optimizer,
            imgsz=imgsz,
            lr0=lr0,
            lrf=lrf,
            epochs=epochs,
            batch=batch,
            augment=augment,
            name=workspace_name, 
            workers=num_workers, 
            save_dir=save_dir
        )

        success = True
        last_model = get_last_model()
        saved_model = save_model(last_model)
        save_model_results(model, saved_model)
        
    except Exception as err:
        logging.error(f'Unexpected Error while training yolov8 - detect: {err}')
    

    return success


if __name__ == "__main__":
    
    
    last_model = Models.objects.get(model_tag='v002')
    TAG = increment(last_model.model_tag)
    
    m = Models()
    m.model_id = increment(last_model.model_id)
    m.model_name = last_model.model_name
    m.sensor_box = last_model.sensor_box
    m.model_tag = TAG
    filename = increment(os.path.basename(last_model.model_file.url))
    m.model_file = get_model_path(m, filename)
    m.save()
    