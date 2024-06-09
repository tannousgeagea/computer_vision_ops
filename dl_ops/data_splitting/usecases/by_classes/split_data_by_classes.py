import os
import random
import numpy as np
from tqdm import tqdm
from data_splitting.utils.tools import split, get_metadata
from utils.config import Annotation, Image, project


def train_val_split():
    metainfo = get_metadata()
    
    if not len(metainfo):
        print('All data are splitted')
        return
    
    for key, value in project.annotation_group.items():
        data = Image.objects.filter(
            annotation__project=project,
            annotation__meta_info__class_id__has_keys=[key]
        )
        
        split(data)


if __name__ == "__main__":
    # specific_class_ids = ["1", "2"]
    # specific_class_ids = specific_class_ids

    # # Filter annotations that contain the specific class_ids
    # annotations_with_specific_class_ids = Annotation.objects.filter(
    #     meta_info__class_ids__has_keys=specific_class_ids
    # )
    
    # print(annotations_with_specific_class_ids.values_list('image', flat=True))
    
    
    # image = Image.objects.filter(id__in=annotations_with_specific_class_ids.values_list('image', flat=True))
    
    
    # Image.objects.all().update(mode='N/A')

    # annotation_group = project.annotation_group
    
    # print(annotation_group)
    
    
    train_val_split()
    