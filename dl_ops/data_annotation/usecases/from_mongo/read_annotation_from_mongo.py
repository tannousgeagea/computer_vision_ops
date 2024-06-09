import os
import django
import logging
from tqdm import tqdm
from utils import mongodb
from datetime import datetime
from utils.config import Image, project, edge_box
from utils.tasks import task_map

params = {
    'user': os.environ.get('MONGO_DB_USER'),
    'passwd': os.environ.get('MONGO_DB_PASSWORD'),
    'server': os.environ.get('MONGO_DB_SERVER'),
    'database_name': os.environ.get('MONGO_DB_DATABASE'),
    'tgt_collection_name': os.environ.get('MONGO_DB_COLLECTION')
}
mongodb_client = mongodb.MongoDBClient(
    db_params=params
)

def get_metainfo():
    return Image.objects.filter(annotated=False)

def fetch_date_from_mongo(image):
    query = {
        'alarm_id': {
            '$eq': image.image_id
        }
    }
    
    count, record = mongodb_client.query(query=query)
    return count, record
    
def extract_data_by_task(image, items, task:str='detect'):
    suc = False
    try:
        task_mapper = task_map()
        annotator = task_mapper[task]['annotator']
        suc = annotator.annotate(image=image, items=items)
    except Exception as err:
        logging.error('Error mapping task to annotation')
    
    return suc
            
def annotate():
    meta_data = get_metainfo()
    
    if not len(meta_data):
        print('All Data are already annotated')
        return
    
    pbar = tqdm(meta_data, ncols=125)
    for image in pbar:
        image_file = image.image_file
        pbar.set_description(f'processing {os.path.basename(image_file.url)}')
        
        count, record = fetch_date_from_mongo(image=image)
        if not count:
            logging.warning(f'⚠️  - Warning: No data can be retrived from mongo')
            continue
        
        matching_items = list(record)
        task = project.project_type
        suc = extract_data_by_task(image, matching_items, task=task)
        if not suc:
            continue
        
        image.annotated = True
        image.save()

    
if __name__ == "__main__":
    annotate()