
import os
import uuid
import time
import django

from datetime import date
from datetime import datetime
from utils.connection import establish_ssh_connection
from utils.connection import create_scp_client
from utils.connection import download_file
from utils.connection import check_remote_file_exists
from utils.connection import list_files_in_directory
from utils.date_utils import days_after_given_date
from utils.config import Image, EdgeBoxInfo
from utils.config import edge_box, src
from data_reader.utils.utils import register_one_image

DATE_FORMAT = '%m-%d-%Y'
HOME = os.environ.get('HOME')
server_ip = os.environ.get('SSH_HOST')
username = os.environ.get('SSH_USERNAME')
password = os.environ.get('SSH_PASSWORD')
sensor_box_id = os.environ.get('sensor_box_id')

def serve():    
    ssh_client = establish_ssh_connection(server_ip, 22, username, password)
    scp_client = create_scp_client(ssh_client)
    last_entry_timestamp = edge_box.meta_info['last_entry_timestamp']
    
    last_entry_timestamp = datetime.strptime(last_entry_timestamp, '%Y-%m-%d').strftime(DATE_FORMAT)
    days = days_after_given_date(start_date=last_entry_timestamp, format=DATE_FORMAT)

    if not len(days):
        print(f'No more days to fetch data from. last entry time stamp: {last_entry_timestamp}')
        
    for day in days:
        extension = f'*{day}*.jpg'
        files_path = list_files_in_directory(ssh_client=ssh_client, remote_directory=src, extension=extension)
        print(f'{len(files_path)} files with {extension} are Found !')
        
        if not len(files_path):
            return
            
        for file in files_path:
            success = register_one_image(filename=os.path.basename(file), image_id=str(uuid.uuid4()), scp_client=scp_client, ssh_client=ssh_client)
        
    edge_box.meta_info['last_entry_timestamp'] = date.today().strftime("%Y-%m-%d")
    edge_box.save()
    
if __name__ == "__main__":
    serve()