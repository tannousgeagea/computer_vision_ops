import os
import math
import time
import django
django.setup()

from typing import Callable
from fastapi import Body
from fastapi import Header
from fastapi import status
from fastapi import Request
from fastapi import Response
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.routing import APIRoute
from datetime import date, timezone
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from typing import Callable, Union, Any, Dict, AnyStr, Optional, List
from typing_extensions import Annotated


from database.models import PlantInfo, EdgeBoxInfo

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
    tags=["EdgeBoxInfo"],
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
    "/edge_box_info/metadata", methods=["GET"], tags=["EdgeBoxInfo"]
)
def get_edge_box_meta_data(response:Response):
    
    metadata = {}
    try:

        edge_box = EdgeBoxInfo.objects.all()
        
        edge_box_data = []
        for edge in edge_box:
            edge_box_data.append(
                {
                    'edge_box_id': edge.edge_box_id,
                    'edge_box_location': edge.edge_box_location,
                }
            )
            
        metadata = {
            'metadata': {
                "edge_box": edge_box_data,
            }
        }

    # except EdgeBoxInfo.DoesNotExist:
    #     metadata['error'] = {
    #         'status_code': 404,
    #         'status_description': f'Matching query for plant {plant} was not found',
    #         'detail': "EdgeBoxInfo matching query does not exist."
    #     }
    #     response.status_code = status.HTTP_404_NOT_FOUND
    
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
