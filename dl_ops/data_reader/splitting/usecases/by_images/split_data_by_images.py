import os
import django
import random
import numpy as np
from tqdm import tqdm
from utils.date_utils import now_str

seed = int(os.environ.get('SEED'))
random.seed(seed)
np.random.seed(seed)


django.setup()
from database.models import Image

def split_by_image(
    data,
    split_ratio=0.2
):  
    
    list_of_ids = list(data.values_list('id', flat=True))
    indexes = random.sample(list_of_ids, len(list_of_ids))
    train = indexes[:-int(split_ratio*len(list_of_ids))]
    val = indexes[-int(split_ratio*len(list_of_ids)):]
    
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
        print(f'{now_str()}: All data are splitted')
        return               

    print(f'{now_str()}: {len(metainfo)} Images are Found')
    split_by_image(data=metainfo)


if __name__ == "__main__":
    meta_info = Image.objects.all().update(mode='N/A')
    train_val_split()