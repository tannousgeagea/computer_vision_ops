import os
import cv2
import logging
import numpy as np
from typing import Any, Iterator, List, Optional, Tuple, Union


def poly2xyxy(poly):
   
   """
    Convert a polygon representation to an axis-aligned bounding box.

    This function takes a list of vertices (x, y) of a polygon and calculates the minimum and 
    maximum x and y coordinates. The result is a bounding box (xmin, ymin, xmax, ymax) that 
    tightly encloses the polygon.

    Parameters:
    - poly (List[Tuple[int, int]]): A list of tuples, where each tuple represents a vertex (x, y) of the polygon.

    Returns:
    - Tuple[int, int, int, int]: A tuple representing the bounding box (xmin, ymin, xmax, ymax) of the polygon.
    """
   poly = np.array(poly)
   return (min(poly[:, 0]), min(poly[:, 1]), max(poly[:, 0]), max(poly[:, 1]))


def xyxy2xywh(xyxy):
    """
    Convert bounding box coordinates from (xmin, ymin, xmax, ymax) format to (x, y, width, height) format.

    Parameters:
    - xyxy (Tuple[int, int, int, int]): A tuple representing the bounding box coordinates in (xmin, ymin, xmax, ymax) format.

    Returns:
    - Tuple[int, int, int, int]: A tuple representing the bounding box in (x, y, width, height) format. 
                                 (x, y) are  the center of the bounding box.
    """
    xmin, ymin, xmax, ymax = xyxy
    w = xmax - xmin
    h = ymax - ymin
    return (xmin + w/2, ymin + h/2, w, h)

def xywh2xyxy(xywh):
    """
    Convert bounding box coordinates from (x, y, width, height) format to (xmin, ymin, xmax, ymax) format.

    This function assumes (x, y) as the center of the bounding box and calculates 
    the coordinates of the top-left corner (xmin, ymin) and the bottom-right corner (xmax, ymax).

    Parameters:
    - xywh (Tuple[float, float, float, float]): A tuple representing the bounding box in (x, y, width, height) format.

    Returns:
    - Tuple[float, float, float, float]: A tuple representing the bounding box in (xmin, ymin, xmax, ymax) format.
    """
    x, y, w, h = xywh
    return (x - w/2, y - h/2, x + w/2, y + h/2)

def xyxyn2xyxy(xyxyn, image_shape):
    """
    Convert bounding box coordinates from normalized format to pixel format.

    This function converts the normalized bounding box coordinates back to pixel format. 
    The normalized coordinates (xmin_n, ymin_n, xmax_n, ymax_n), represented as fractions 
    of the image's width or height, are scaled back to the pixel dimensions of the image.

    Parameters:
    - xyxyn (tuple): A tuple of four floats (xmin_n, ymin_n, xmax_n, ymax_n) representing the normalized bounding box coordinates.
    - image_shape (tuple): A tuple of two integers (height, width) representing the dimensions of the image.

    Returns:
    - tuple: A tuple of four integers (xmin, ymin, xmax, ymax) representing the bounding box coordinates in pixel format.
    """
    xmin, ymin, xmax, ymax = xyxyn
    return (int(xmin * image_shape[1]), int(ymin * image_shape[0]), int(xmax * image_shape[1]), int(ymax * image_shape[0]))
