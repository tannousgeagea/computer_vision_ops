import os
import random
import numpy as np
from utils.config import Image, project


seed = int(os.environ.get('SEED'))
random.seed(seed)
np.random.seed(seed)

def split(
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
    images = Image.objects.filter(
        annotation__project=project
    ).exclude(mode__in=['train', 'val']).distinct()
    
    return images