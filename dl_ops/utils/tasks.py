
from data_annotation.task.detect import annotate_for_detection
from data_annotation.task.classify import annotate_for_classification
from data_annotation.task.segment import annotate_for_segmentation

tasks = ['detect', 'segment', 'classify']

def task_map():
    return {
        'classify': {
            'annotator': annotate_for_classification,
        },
        
        'detect': {
            'annotator': annotate_for_detection,
        },
        
        'segment': {
            'annotator': annotate_for_segmentation
        }
    }