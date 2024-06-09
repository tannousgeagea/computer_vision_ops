import os

import models
import models.usecases
import models.usecases.yolov8
import models.usecases.yolov8.tasks
import models.usecases.yolov8.tasks.detect
import models.usecases.yolov8.tasks.detect.trainer

cases_map = {
    'yolov8-detect': models.usecases.yolov8.tasks.detect.trainer
}

def main(case):
    assert case in cases_map.keys(), f'Unsupported case. expected one of {list(cases_map.keys())}, got {case}'
    
    trainer = cases_map[case]
    trainer.train()
    
if __name__ == '__main__':
    main('yolov8-detect')
    