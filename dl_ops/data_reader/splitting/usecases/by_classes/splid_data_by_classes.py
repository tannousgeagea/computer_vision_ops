import os
import django
import random
import numpy as np
from tqdm import tqdm

seed = int(os.environ.get('SEED'))
random.seed(seed)
np.random.seed(seed)


django.setup()
from database.models import Objects, Image

def split_by_class(
    data,
    split_ratio=0.2
):
    keys = list(data.keys())
    for k, v in data.items():
        indexes = random.sample(v, len(v))
        train = indexes[:-int(split_ratio*len(v))]
        val = indexes[-int(split_ratio*len(v)):]
        
        Image.objects.filter(id__in=train).update(mode='train')
        Image.objects.filter(id__in=val).update(mode='val')


def get_metadata():
    return Image.objects.filter(annotated=True).exclude(mode__in=['train', 'val'])

def write_result(data, key, value):
    if not key in data.keys():
        data[key] = []    
    data[key].append(value)
    
    return data

def train_val_split():
    metainfo = get_metadata()
    
    if not len(metainfo):
        print('All data are splitted')
        return
    
    data = {}
    for image in metainfo:
        object_model = Objects.objects.filter(image=image)
        
        for object in object_model:
               object_class = object.object_class
               data = write_result(data, key=object_class, value=image.id)
               

    split_by_class(data=data)


if __name__ == "__main__":
    meta_info = Image.objects.all()
    
    for image in meta_info:
        image.mode = 'N/A'
        image.save()
