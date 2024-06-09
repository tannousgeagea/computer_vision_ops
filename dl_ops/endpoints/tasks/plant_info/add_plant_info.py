import os
import django
django.setup()
from celery import shared_task
from datetime import datetime, timezone
from database.models import PlantInfo
from typing import Union, List


def check_request(objects:dict, keys:Union[str, List]):
    assert isinstance(objects, dict), f'objects are expected to be of type dict, but got {type(objects)}'
    for key in keys if isinstance(keys, list) else [keys]:
        assert key in objects.keys(), f'key {key} not found in objects'

@shared_task(bind=True,autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5}, ignore_result=True,
             name='plant_info:add_new_plant_info_entry')
def add_new_plant_info_entry(self, **kwargs):
    data:dict = {}
    try:
        request = kwargs
        plant_info = PlantInfo()
        
        check_request(
            request,
            keys=[
                'plant_id',
                'plant_name',
                'plant_location',
            ]
        )
        
        plant_id = request.get('plant_id')
        if PlantInfo.objects.filter(plant_id=plant_id).exists():
            data.update(
                {
                    "action": "failed",
                    "time": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
                    "result": f"Failed to add new entry: plant_id {plant_id} already exists", 
                }
            )
            return data
        
        plant_info.plant_id = plant_id
        plant_info.plant_name = request.get('plant_name')
        plant_info.plant_location = request.get('plant_location')
        plant_info.save()
        
        data.update(
            {
                'action': 'done',
                'time': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
                'result': f"Successfully added new plant info with plant_id {plant_id}"
            }
        )
    
    except Exception as e:
        data.update(
            {
                "action": "failed",
                "time": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
                "result": f"Failed to add new entry: {str(e)}", 
            }
        )
        
    return data