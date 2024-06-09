import os
import cv2
import uuid
import django
import random
django.setup()

from tqdm import tqdm
from utils.convertor import xywh2xyxy, xyxyn2xyxy
from utils.annotate import Annotator
from database.models import Image
from utils.data_utils import load_image, load_label, save_label, save_image, rectify_labels
from augmentation.tasks.detect.augment import Augmentation


augmentation_album = [
    'HorizontalFlip',
    'RandomBrightnessContrast',
    'VerticalFlip',
    'Flip',
    'OpticalDistortion',
    'ChannelShuffle',
    'ChannelDropout',
    'Rotate',
    'ShiftScaleRotate',
]

variant =  3
augmentation = Augmentation()
out = os.environ.get('SRC_TRAIN_VAL')

def get_metadata():
    return Image.objects.filter(mode='train')

def augment():
    metadata = get_metadata()
    pbar = tqdm(metadata, ncols=125)
    for image in pbar:
        # pbar.set_description('Augmentation:')
        cv_image = load_image(image.image_file.url)
        labels = load_label(image.annotation.url)
        # im, labels = augmentation(im=cv_image, labels=labels)
        im = cv_image
        selected_augmentation = random.sample(augmentation_album, variant)
        for aug in selected_augmentation: 
            pbar.set_description(f'{aug}')
            if not len(labels):
                continue
            try:
                new_im, new_labels = augmentation.augment(im, labels, choice=aug, p=1)
                file_name = os.path.basename(image.annotation.url).split('.txt')[0] + f'.{str(uuid.uuid4())}'
                save_label(new_labels.tolist(), out + '/train/labels/' + file_name + '.txt')
                save_image(new_im, out + "/train/images/" + file_name + '.jpg')
            
            except Exception as err:
                pbar.write(f'{err}')

if __name__ == "__main__":
    augment()
        
        
        