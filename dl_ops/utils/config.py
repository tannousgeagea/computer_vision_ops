import os
import uuid
import time
import django
django.setup()

from datetime import datetime
from database.models import EdgeBoxInfo,  Image
from database.models import Annotation, Project, DataVersion, ImageDataVersion
from database.models import Model, ModelVersion, ModelMetric, ModelEval

out = os.environ.get('OUT')
DATETIME_FORTMAT = '%Y-%m-%d %H:%M:%S'
sensor_box_id = 'wae-a01-00002'
model_id = 'yolov8.impurity.v001'

edge_box = EdgeBoxInfo.objects.get(edge_box_id=sensor_box_id)
project = Project.objects.get(edge_box=edge_box, project_id='wasteant-impurity-detection-gml-luh-001')

configuration = project.config
src = configuration.get('src')
default_query = configuration.get('mongo-query')
data_acquisition_mode = configuration.get('data-acquisition-mode')
data_annotation_mode = configuration.get('data-annotation-mode')
data_splitting_mode = configuration.get('data-splitting-mode')
tasks = ['detect', 'segment', 'classify']