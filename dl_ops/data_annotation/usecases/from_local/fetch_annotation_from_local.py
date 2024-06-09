import os
import shutil
import django
import logging
from tqdm import tqdm
from datetime import datetime
from utils.convertor import xyxy2xywh
from utils.convertor import poly2xyxy
from utils.config import src, out, project
from utils.data_utils import load_label
from utils.common import get_label_path
from utils.config import Image, Annotation

def get_metainfo():
    return Image.objects.filter(annotated=False)

def fetch_label_from_local(image):
    suc = False
    try:
        ext = os.path.basename(image.image_file.url).split('.')[-1]
        file_name = os.path.basename(image.image_file.url).split(f'.{ext}')[0] + '.txt'
        label = src + "/labels/" + file_name

        if not os.path.exists(label):
            logging.warning(f'⚠️  - Warning: No data can be retrived from local: {label}')
            return suc
        
        if Annotation.objects.filter(project=project, image=image).exists():
            annotation = Annotation.objects.get(project=project, image=image)
        else:
            annotation = Annotation(image=image, project=project)
            
        path_to_txt_files = out + '/' + get_label_path(annotation, filename=file_name)
        if not os.path.exists(os.path.dirname(path_to_txt_files)):
            os.makedirs(os.path.dirname(path_to_txt_files))
            
        shutil.move(label, path_to_txt_files)
        annotation.annotation_file = get_label_path(annotation, filename=file_name)
        annotation.save()
        suc = True
        
    except Exception as err:
        logging.error(f'Error encouterd: {err}')
    
    return suc
        
def annotate():
    ann_suc = False
    try:
        meta_data = get_metainfo()
        if not len(meta_data):
            print('All Data are already annotated')
            return ann_suc
        
        pbar = tqdm(meta_data, ncols=125)
        for image in pbar:
            image_file = image.image_file
            pbar.set_description(f'processing {os.path.basename(image_file.url)}')
            
            suc = fetch_label_from_local(image=image)
            if not suc:
                return ann_suc
            
            image.annotated = True
            image.save()
            ann_suc = True            
    except Exception as err:
        logging.error(f'Error encouterd whilt fetching data from local: {err}')

    return ann_suc

    