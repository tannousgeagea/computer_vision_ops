import os
import uuid
import shutil
from glob import glob
from tqdm import tqdm
from datetime import date
from utils.config import edge_box, src
from data_reader.utils.common import register_one_image

def serve():
    files_path = glob(src + "/images/*.jpg")

    print(f'{len(files_path)} files are Found in {src} !')
    
    if not len(files_path):
        return
        
    pbar = tqdm(files_path, ncols=125)
    for file in pbar:
        pbar.set_description(f'processing {file}')
        success = register_one_image(filename=os.path.basename(file), image_id=str(uuid.uuid4()), local=True)

    edge_box.last_entry_timestamp = date.today()
    edge_box.save()