import os
import math
import time
import django
django.setup()
from datetime import datetime, timedelta
from datetime import date, timezone
from typing import Callable
from fastapi import Request
from fastapi import Response
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi import status
from typing import Callable, Union, Any, Dict, AnyStr, Optional, List
from typing_extensions import Annotated
from fastapi import Body
from fastapi import Header

from database.models import PlantInfo, EdgeBoxInfo
from endpoints.tasks.plant_info.add_plant_info import add_new_plant_info_entry

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


router = APIRouter(
    prefix="/api/v1",
    tags=["PlantInfo"],
    route_class=TimedRoute,
    responses={404: {"description": "Not found"}},
)

class ApiResponse(BaseModel):
    status: str
    task_id: str
    data: Optional[Dict[AnyStr, Any]] = None


class ApiRequest(BaseModel):
    request: Optional[Dict[AnyStr, Any]] = None



@router.api_route(
    "/plant_info/metadata", methods=["GET"], tags=["PlantInfo"]
)
def get_plant_meta_data(response:Response):
    
    metadata = {}
    try:
        plant_info = PlantInfo.objects.all()
        
        plant_data = []
        for plant in plant_info:
            edge_box = EdgeBoxInfo.objects.filter(plant=plant)
            
            edge_box_data = []
            for edge in edge_box:
                edge_box_data.append(
                    {
                        'edge_box_id': edge.edge_box_id,
                        'edge_box_location': edge.edge_box_location,
                    }
                )
                
            plant_data.append(
                {
                    'plant_name': plant.plant_name,
                    'plant_id': plant.plant_id,
                    'plant_location': plant.plant_location,
                    'edge_box': edge_box_data,
                    
                }
            )
            
        metadata = {
            'metadata': {
                "plant": plant_data,
            }
        }

    except EdgeBoxInfo.DoesNotExist:
        metadata['error'] = {
            'status_code': 404,
            'status_description': f'Matching query for plant {plant} was not found',
            'detail': "EdgeBoxInfo matching query does not exist."
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    
    except HTTPException as e:
        metadata['error'] = {
            "status_code": 404,
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    
    except Exception as e:
        metadata['error'] = {
            'status_code': 500,
            "status_description": "Internal Server Error",
            "detail": str(e),
        }
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
    return metadata


    
@router.api_route(
    "/plant_info/{plant_id}", methods=['GET'], tags=['PlantInfo']
)
def get_plant_info_from_plant_id(response:Response, plant_id:str):
    results = {}
    try:
        plant_info = PlantInfo.objects.filter(plant_id=plant_id)
        
        plant_data = []
        for plant in plant_info:
            edge_box = EdgeBoxInfo.objects.filter(plant=plant)
            
            edge_box_data = []
            for edge in edge_box:
                edge_box_data.append(
                    {
                        'edge_box_id': edge.edge_box_id,
                        'edge_box_location': edge.edge_box_location,
                    }
                )
                
            plant_data.append(
                {
                    'plant_name': plant.plant_name,
                    'plant_id': plant.plant_id,
                    'plant_location': plant.plant_location,
                    'edge_box': edge_box_data,
                    
                }
            )
            
        results = {
            'metadata': {
                "plant": plant_data,
            }
        }

    except PlantInfo.DoesNotExist:
        results['error'] = {
            'status_code': 404,
            'status_description': f'Matching query for plant_id {plant_id} was not found',
            'detail': "PlantInfo matching query does not exist."
        }
        response.status_code = status.HTTP_404_NOT_FOUND

    except EdgeBoxInfo.DoesNotExist:
        results['error'] = {
            'status_code': 404,
            'status_description': f'Matching query for plant {plant} was not found',
            'detail': "EdgeBoxInfo matching query does not exist."
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    
    except HTTPException as e:
        results['error'] = {
            "status_code": 404,
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    
    except Exception as e:
        results['error'] = {
            'status_code': 500,
            "status_description": "Internal Server Error",
            "detail": str(e),
        }
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
    return results


@router.api_route(
    "/plant_info/new_entry", methods=['POST'], tags=['PlantInfo']
)
async def add_plant_info(
    payload: ApiRequest = Body(...),
    x_request_id: Annotated[Optional[str], Header()] = None,
) -> ApiResponse:
    
    try:
        if not payload.request:
            raise HTTPException(status_code=400, detail="Invalid request payload")
        
        print(payload.request)
        task = add_new_plant_info_entry.apply_async(kwargs=payload.request, task_id=x_request_id)
        response_data = {
            "status": "success",
            "task_id": task.id,
            "data": payload.request
        }
    
    except Exception as e:
        response_data = {
            "status": 'Failed',
            "task_id": "",
            "data": {
                "error": {
                    "status_code": 404,
                    "status_description": "",
                    "detail": str(e),
                }
            }
        }
    
    return ApiResponse(**response_data)

