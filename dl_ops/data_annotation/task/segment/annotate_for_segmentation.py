import os
import logging
import numpy as np
from tqdm import tqdm
from utils.convertor import xyxy2xywh
from utils.convertor import poly2xyxy
from utils.common import extract_annotation
from utils.common import get_label_path
from utils.config import (
    Annotation, project, out, tasks
)


def annotate(image, items):

    suc = False
    try:
        suc, annotation_data = extract_annotation(items, task='segment')
        if not suc:
            return suc
        
        lines = []
        for i, cls_id in enumerate(annotation_data['class_id']):
            xyn  = np.array(annotation_data['xyn'][i]).flatten().tolist()
            line = (cls_id, *xyn)

            lines.append(("%g " * len(line)).rstrip() %line + "\n")
        
        if Annotation.objects.filter(project=project, image=image).exists():
            labels = Annotation.objects.get(project=project, image=image)
        else:
            labels = Annotation(image=image, project=project)
            
        file_name = os.path.basename(image.image_file.url).split('.jpg')[0] + '.txt'
        labels.annotation_file = get_label_path(labels, file_name)  
        
        path_to_txt_files = out + "/" + get_label_path(labels, file_name) 
        if not os.path.exists(os.path.dirname(path_to_txt_files)):
            os.makedirs(os.path.dirname(path_to_txt_files))

        with open(path_to_txt_files, "w") as f:
            f.writelines(lines)

        labels.save()
        suc = True
    except Exception as err:
        logging.error(f'Error while annotating data for detect task: {err}')
    
    return suc

