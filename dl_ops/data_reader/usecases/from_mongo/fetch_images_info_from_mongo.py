
import os
import uuid
import time

import logging
from tqdm import tqdm
from datetime import date
from utils import mongodb
from datetime import datetime, timedelta
from utils.connection import establish_ssh_connection
from utils.connection import create_scp_client
from utils.date_utils import days_after_given_date, datetimefday
from utils.common import get_image_path
from utils.config import edge_box, src, default_query
from data_reader.utils.utils import register_one_image

DATE_FORMAT = '%Y-%m-%d'
server_ip = "10.10.0.29" #os.environ.get('SSH_HOST')
username = os.environ.get('SSH_USERNAME')
password = os.environ.get('SSH_PASSWORD')

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

def fetch_info_from_mongo(start_day, end_day):
    query = {
        **default_query,
        'header.timestamp': {
            '$gte': start_day,
            '$lte': end_day,
        }
    }
    
    count, record = mongodb_client.query(query=query)
    
    return count, record

def serve():    
    ssh_client = establish_ssh_connection(server_ip, 22, username, password)
    scp_client = create_scp_client(ssh_client)
    last_entry_timestamp = edge_box.meta_info['last_entry_timestamp']
    
    days = days_after_given_date(start_date=last_entry_timestamp, format=DATE_FORMAT)

    if not len(days):
        print(f'No more days to fetch data from. last entry time stamp: {last_entry_timestamp}')
        return
    
    print(f'Starting Day: {days[0]}')
    print(f'Ending Day: {days[-1]}')
    
    start_date = datetimefday(day=days[0], format=DATE_FORMAT)
    end_date = datetimefday(day=days[-1], format=DATE_FORMAT) + timedelta(days=1)
    count, record = fetch_info_from_mongo(start_day=start_date, end_day=end_date)
    
    try:
        pbar = tqdm(range(count), ncols=225)
        for i in pbar:
            alarm_id = record[i]['alarm_id']
            contents = record[i]['content']
            pbar.set_description(f'processing {alarm_id}')
            for content in contents:
                file = content['assets']['location']
                file = src + "/" + os.path.basename(file).replace('.jpg', '_orig.jpg')               
                filename = os.path.basename(file)
                success = register_one_image(filename, image_id=alarm_id, ssh_client=ssh_client, scp_client=scp_client)
            
        edge_box.meta_info['last_entry_timestamp'] = date.today().strftime("%Y-%m-%d")
        edge_box.save()
    except Exception as err:
        logging.error('Error: %s' %err)
        
if __name__ == "__main__":
    serve()
    
    