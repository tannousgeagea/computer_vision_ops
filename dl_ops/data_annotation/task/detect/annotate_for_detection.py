import os
import logging
import numpy as np
from tqdm import tqdm
from utils.convertor import xyxy2xywh
from utils.convertor import poly2xyxy
from utils.common import get_label_path
from utils.common import extract_annotation, write_result
from utils.config import (
    Annotation, project, out, tasks
)


annotation_group = project.annotation_group


def annotate(image, items):

    suc = False
    try:
        suc, annotation_data = extract_annotation(items, task='detect')
        if not suc:
            return suc
        
        lines = []
        class_id = {}
        for i, cls_id in enumerate(annotation_data['class_id']):
            
            print(annotation_group[str(cls_id)])
            class_id = write_result(data=class_id, key=cls_id, value=annotation_group[str(cls_id)], value_format='str')
            if cls_id <  0:
                continue
            
            xywh  = xyxy2xywh(annotation_data['xyxyn'][i])
            line = (cls_id, *xywh)
            lines.append(("%g " * len(line)).rstrip() %line + "\n")
        
        if Annotation.objects.filter(project=project, image=image).exists():
            labels = Annotation.objects.get(project=project, image=image)
        else:
            labels = Annotation(image=image, project=project)
            
        file_name = os.path.basename(image.image_file.url).split('.jpg')[0] + '.txt'
        labels.annotation_file = get_label_path(labels, file_name)  
        labels.meta_info = {
            'class_id': class_id
        }
        
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

