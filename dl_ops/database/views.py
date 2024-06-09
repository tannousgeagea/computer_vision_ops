import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Image, EdgeBoxInfo, Annotation
from utils.data_utils import load_label
from utils.convertor import xywh2xyxy, xyxyn2xyxy

# Create your views here.
senser_box_id = os.environ.get('sensor_box_id')
local_file = '/home/waminion09/WA_Development/wa_incremental_learning_impurity_detection/data/images'


def read_data(request):
    data = []
    # edge_box = EdgeBoxInfo.objects.get(sensor_box_id=senser_box_id)
    images = Image.objects.filter(annotated=True).order_by('-entry_timestamp')
    
    
    for image in images:
        label = load_label(image.annotation.url).tolist()
        annotation = []
        for lb in label:
            xyxyn = xywh2xyxy(lb[1:])
            # xyxy = xyxyn2xyxy(xyxyn, image_shape=(1536, 2048))
            
            annotation.append(
                {
                    'label': Annotation.objects.get(object_class_id=lb[0]).object_class_name,
                    'coordinates': {'x': xyxyn[0], 'y': xyxyn[1], 'width': xyxyn[2] - xyxyn[0], 'height': xyxyn[3] - xyxyn[1]}
                }
            )
        data.append(
            {   'date': image.entry_timestamp.strftime('%Y-%m-%d'),
                'image_id': image.id,
                'image_url': image.image_file.url,
                "annotations": annotation
            }
        )
        
    return JsonResponse(data=data, safe=False)

def serve_dashboard(request):
    return render(request, "/home/appuser/src/dl_ops/template/image_wrapper.html")