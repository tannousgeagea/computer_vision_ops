import os
import cv2
import shutil
import numpy as np
import logging

def load_image(file):
    im = cv2.imread(file)
    assert im is not None, f"Image Not Found {file}"
    
    return im

def load_label(file):
    """
    Extract bounding box data from a text file.

    This function reads a text file containing bounding box data. Each line in the file should 
    represent a bounding box or a polygon, starting with a class ID followed by the vertices coordinates.
    If a line contains more than 4 coordinates, it is treated as a polygon and converted to an axis-aligned
    bounding box. The function returns class IDs and bounding boxes.

    Parameters:
    - txt_file (str): The path to the text file containing the bounding box data.

    Returns:
    - A tuple of two lists, the first being class IDs and 
      the second being bounding boxes (each box either as (xmin, ymin, xmax, ymax) or as a polygon)
    """
    assert os.path.exists(file) ,f'File Not Found {file}'
    
    with open(file) as f:
        lb = [x.split() for x in f.read().strip().splitlines() if len(x)]
        lb = np.array(lb, dtype=np.float32)
        
    nl = len(lb)
    if nl:
        assert lb.shape[1] == 5, f"labels require 5 columns, {lb.shape[1]} columns detected"
        assert (lb >= 0).all(), f"negative label values {lb[lb < 0]}"
        assert (lb[:, 1:] <= 1).all(), f"non-normalized or out of bounds coordinates {lb[:, 1:][lb[:, 1:] > 1]}"
        _, i = np.unique(lb, axis=0, return_index=True)
        if len(i) < nl:  # duplicate row check
            lb = lb[i]  # remove duplicates
            msg = f"WARNING ⚠️ {file}: {nl - len(i)} duplicate labels removed"
            print(msg)
    else:
        lb = np.zeros((0, 5), dtype=np.float32)
    
    return lb


def save_label(labels, file):
    lines = [("%g " * len(line)).rstrip() % tuple(line) + "\n" for line in labels]
    
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    
    with open(file, "w") as f:
        f.writelines(lines)
        
def save_image(im, file):
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    
    cv2.imwrite(file, im)
    
    
def modify_annotation_in_txt_file(txt_file:str, src_class:list, dest_cls:list):
    if not os.path.exists(txt_file):
        logging.error('File Not Found %s' %txt_file)
        return False
    
    labels = load_label(txt_file)
    if isinstance(src_class, int):
        src_class = [src_class]
    
    if isinstance(dest_cls, int):
        dest_cls =  [dest_cls]
    
    assert len(src_class) == len(dest_cls), f'src_class and dest_class must have the same lenght: {len(src_class)} != {len(dest_cls)}'
    
    lines = []
    for i, label in enumerate(labels):
        if int(label[0]) in src_class:
            index = src_class.index(int(label[0]))
            label[0] = dest_cls[index]
        
        label = tuple(label.tolist())
        lines.append(("%g " * len(label)).rstrip() %label + "\n")
            
    with open(txt_file, 'w') as f:
        f.writelines(lines)
        
    return True

def fetch_image_from_local(src, destination):
    success = False

    if not os.path.exists(src):
        logging.error(f'File {src} does not exist')
        return success
        
    try:
        shutil.move(src, destination)
        success = True
    except Exception as err:
        logging.error(f'Unexpected error in fetching image {src} from local: {err}')
    
    return success


def rectify_labels(labels, eps=7e-3):
    labels[:, 1:] = np.array([lb + eps for lb in labels[:, 1:]])
    return labels


if __name__ == "__main__":
    from glob import glob
    files = glob('/media/unregistered_data/labels/*.txt')
    
    for file in files:
        suc = modify_annotation_in_txt_file(txt_file=file, src_class=[1, 2], dest_cls=[0, 0])
        

def get_model_path(instance, filename):
    return f'models/{instance.model_name}/{instance.model_tag}/{filename}'