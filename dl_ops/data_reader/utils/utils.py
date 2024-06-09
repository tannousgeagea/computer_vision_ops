import os
import shutil
import logging
from tqdm import tqdm
from utils.config import Image, edge_box, out, src
from utils.common import get_image_path
from utils.connection import fetch_image_from_server


def fetch_image_from_local(src, destination):
    success = False
    try:
        if os.path.exists(src):
            shutil.move(src, destination)
            success = True
    except Exception as err:
        raise ValueError(f'Unexpected error in fetching image {src} from local: {err}')
    
    return success

def register_one_image(filename:str, image_id:str, ssh_client=None, scp_client=None, local:bool=False):
    suc = False
    try:
        image_model = Image()
        image_model.edge_box = edge_box
        image_model.image_id = image_id
        image_model.image_file = get_image_path(image_model, filename)
                        
        if Image.objects.filter(image_file=image_model.image_file).exists():
            tqdm.write(f'File {filename} already exists - skip')    
            return suc
        
        if not os.path.exists(os.path.dirname(out + "/" + get_image_path(image_model, filename))):
            os.makedirs(os.path.dirname(out + "/" + get_image_path(image_model, filename)))
        
        
        if not local:
            success = fetch_image_from_server(ssh_client, scp_client, src + "/" + filename, local_path=out + "/" + get_image_path(image_model, filename))
        else:
            success = fetch_image_from_local(src=src + "/" + filename, destination=out + "/" + get_image_path(image_model, filename))
            
        if not success:
            tqdm.write(f'Failed to fetch image {filename}')
            return suc

        image_model.save()
        suc = True
    except Exception as err:
        logging.error(f'Error registeing Image: {err}')

    return suc