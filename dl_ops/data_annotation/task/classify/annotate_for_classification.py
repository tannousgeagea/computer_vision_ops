import os
import logging
import numpy as np
from tqdm import tqdm
from data_annotation.utils.common import extract_annotation
from utils.common import get_label_path
from utils.config import (
    Annotation, project, out, tasks
)


def annotate(image, items):
    suc = False
    try:
        annotation_suc, annotation_data = extract_annotation(items, task='classify')
        if not annotation_suc:
            return suc
        
        lines = []
        for i, cls_id in enumerate(annotation_data['class_id']):
            line = (cls_id,)
            lines.append(("%g " * len(line)).rstrip() %line + "\n")
        
        if Annotation.objects.filter(project=project, image=image).exists():
            labels = Annotation.objects.get(project=project, image=image)
        else:
            labels = Annotation(image=image, project=project)
            
        file_name = os.path.basename(image.image_file.url).split('.jpg')[0] + '.txt'
        labels.annotation_file = get_label_path(labels, file_name)  
        labels.meta_info = {
            "class_id": annotation_data['class_id'],
        }
        path_to_txt_files = out + "/" + get_label_path(labels, file_name) 
        if not os.path.exists(os.path.dirname(path_to_txt_files)):
            os.makedirs(os.path.dirname(path_to_txt_files))

        with open(path_to_txt_files, "w") as f:
            f.writelines(lines)

        labels.save()
        suc = True
    except Exception as err:
        logging.error(f'Error while annotating data for classify task: {err}')
        
    return suc

