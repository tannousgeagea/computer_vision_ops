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

def map_class_id(severity_level, ack_status):
    class_ids = {
        '0': 'background',
        '1': 0,
        '2': 0,
        '3': 0,
    }
    index = str(severity_level) if ack_status>0 else str(ack_status)
    
    return class_ids[index]

def extract_annotation(mongo_record:list, task:str='detect'):
    results = {
        'class_id': [],
        'xyxyn': [],
        'xyn': [],
    }
    
    suc = False
    try:
        assert task in tasks, f'task must be one of {tasks}'
        for i in range(len(mongo_record)):
            ack_status = mongo_record[i]['header']['ack_status']
            if ack_status == -1:
                ts = mongo_record[i]['header']['timestamp']
                tqdm.write(f'⚠️  - Warning: Data at {ts} are not labeled yet !')
                return suc, results
            
            severity_level = mongo_record[i]['header']['severity_level']
            class_id = map_class_id(severity_level=severity_level, ack_status=ack_status)
            
            if class_id == 'background':
                results['class_id'] =  [-1]
                continue
            
            if task in ['detect', 'segment']:
                logs = mongo_record[i]['logs']
                for log in logs:
                    xyn = [(log[k], log[k+1]) for k in range(0, len(log), 2)] # (x, y)
                    xyxyn = poly2xyxy(xyn)
                    
                    results['xyn'].append(xyn)
                    results['xyxyn'].append(xyxyn)
                    results['class_id'].append(class_id)
            else:
                results['class_id'].append(class_id)
            
        suc = True
    
    except Exception as err:
        logging.error(f'Error while extracting annotation: {err}')
        
    return suc, results


def write_result(data, key, value, value_format='list'):
    if value_format == "list":
        if not key in data.keys():
            data[key] = []    
        data[key].append(value)
        
    elif value_format == "str":
        data[key] = value
    
    return data