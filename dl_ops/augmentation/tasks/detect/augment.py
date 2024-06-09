'''
 * Copyright (C) WasteAnt - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited.
 * Proprietary and confidential
 * See accompanying/further LICENSES below or attached
 * Created by Tannous Geagea <tannous.geagea@wasteant.com>, September 2023
 * Edited by:
 *
'''

import os
import cv2
import sys
import json
import yaml
import time
import shutil
import random
import logging
import numpy as np
from tqdm import tqdm
from glob import glob
import albumentations as A
from datetime import datetime, date, timedelta

class Augmentation:
    def __init__(
        self, config_params=None,
        augmentation_album=[],
        format='yolo',
        size=640,
    ):
        self.config_params = config_params
        self.augmentation_album = augmentation_album
        self.format = format

        if not self.config_params is None:
            self.augmentation_album = self.config_params['augmentation_album'] if 'augmentation_album' in self.config_params.keys() else self.config_params
            self.format = self.config_params['format'] if 'format' in self.config_params.keys() else self.format

        try:
            T = [
                A.RandomResizedCrop(height=size, width=size, scale=(0.8, 1.0), ratio=(0.9, 1.11), p=0.0),
                A.Blur(p=0.01),
                A.MedianBlur(p=0.01),
                A.ToGray(p=0.01),
                A.CLAHE(p=0.01),
                A.RandomBrightnessContrast(p=0.0),
                A.RandomGamma(p=0.0),
                A.ImageCompression(quality_lower=75, p=0.0),
            ]  # transforms

            self.transform = A.Compose(T, bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
            print(", ".join(f"{x}".replace("always_apply=False, ", "") for x in T if x.p))

        except Exception as err:
            logging.error(f'Unexpected Error in augmentation: {err}')

    def __call__(self, im, labels, p=1.0):
        """Applies transformations to an image and labels with probability `p`, returning updated image and labels."""
        if self.transform and random.random() < p:
            new = self.transform(image=im, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
            im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels
    
    def apply_horizantal_flip(self, image, labels, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.HorizontalFlip(p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels
    
    def apply_vertical_filp(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.VerticalFlip(p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels

    def apply_flip(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.Flip(p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels
        
    def apply_shift_scale_rotate(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.ShiftScaleRotate(p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels

    def apply_random_brightness_contrast(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.1, p=0.5),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels

    def apply_rotate(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.Rotate(limit=30, p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels


    def apply_optical_distortion(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.OpticalDistortion(p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels

    def apply_channel_shuffle(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.ChannelShuffle(p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels

    
    def apply_channel_dropout(self, image, labels=None, p=0.5):
        # For bounding box detection task
        transform = A.Compose([
            A.ChannelDropout(p=p),
        ], bbox_params=A.BboxParams(format=self.format, label_fields=["class_labels"]))
        new = transform(image=image, bboxes=labels[:, 1:], class_labels=labels[:, 0])  # transformed
        im, labels = new["image"], np.array([[c, *b] for c, b in zip(new["class_labels"], new["bboxes"])])
            
        return im, labels
            

    def augment(self, image, labels=None, choice=None, p=0.5):
        if choice=="HorizontalFlip":
            image, labels = self.apply_horizantal_flip(image, labels, p)
        elif choice=="RandomBrightnessContrast":
            image, labels = self.apply_random_brightness_contrast(image, labels, p)
        elif choice=="VerticalFlip":
            image, labels = self.apply_vertical_filp(image, labels, p)
        elif choice=="Flip":
            image, labels = self.apply_flip(image, labels, p)
        elif choice=="OpticalDistortion":
            image, labels = self.apply_optical_distortion(image, labels, p)
        elif choice=="ChannelShuffle":
            image, labels = self.apply_channel_shuffle(image, labels, p)
        elif choice=="ChannelDropout":
            image, labels = self.apply_channel_dropout(image, labels, p)
        elif choice=="Rotate":
            image, labels = self.apply_rotate(image, labels, p)
        elif choice=='ShiftScaleRotate':
            image, labels = self.apply_shift_scale_rotate(image, labels, p)
        elif choice=="StrongAugmentation":
            image, labels = self.apply_strong_augmentation(image, labels, p)
        elif choice=="RandomAugmentation":
            image, labels = self.apply_random_augmentation(image, labels, p)
        else:
            logging.warning(f'{choice} is not defined')
            
        return image, labels

