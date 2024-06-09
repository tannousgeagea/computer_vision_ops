import os
import uuid
import time
import logging
from utils.convertor import xyxy2xywh
from utils.convertor import poly2xyxy

tasks = ['detect', 'segment', 'classify']

def get_model_path(instance, filename):
    model = instance.model
    project = model.project
    edge_box = project.edge_box
    return f'{edge_box.edge_box_id}/{project.project_id}/models/{model.model_name}/{instance.model_version}/{filename}'

def get_image_path(instance, filename):
    return f'{instance.edge_box.edge_box_id}/images/{filename}'

def get_label_path(instance, filename):
    image = instance.image
    project = instance.project
    edge_box = image.edge_box
    return f'{edge_box.edge_box_id}/{project.project_id}/annotations/{filename}'


def write_result(data, key, value, value_format='list'):
    if value_format == "list":
        if not key in data.keys():
            data[key] = []    
        data[key].append(value)
        
    elif value_format == "str":
        data[key] = value
    
    return data