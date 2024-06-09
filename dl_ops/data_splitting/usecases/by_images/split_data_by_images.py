import os
import django
import random
import numpy as np
from tqdm import tqdm
from utils.config import Image, Annotation, edge_box, project
from utils.date_utils import now_str
from data_splitting.utils.common import split, get_metadata


def train_val_split():
    metainfo = get_metadata()
    
    if not len(metainfo):
        print(f'{now_str()}: All data are splitted')
        return               

    print(f'{now_str()}: {len(metainfo)} Images are Found')
    split(data=metainfo)


if __name__ == "__main__":
    train_val_split()