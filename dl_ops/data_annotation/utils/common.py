import logging
from tqdm import tqdm
from utils.config import tasks, map_class_id
from utils.convertor import poly2xyxy

tasks = ['detect', 'segment', 'classify']

def extract_annotation(mongo_record:list, task:str='detect'):
    results = {
        'class_id': [],
        'xyxyn': [],
        'xyn': [],
    }
    
    suc = False
    try:
        assert task in tasks, f'task must be one of {tasks}'
        for i in range(len(mongo_record)):
            ack_status = mongo_record[i]['header']['ack_status']
            if ack_status == -1:
                ts = mongo_record[i]['header']['timestamp']
                tqdm.write(f'⚠️  - Warning: Data at {ts} are not labeled yet !')
                return suc, results
            
            severity_level = mongo_record[i]['header']['severity_level']
            class_id = map_class_id(severity_level=severity_level, ack_status=ack_status)
            
            if class_id == 'background':
                results['class_id'] =  [-1]
                continue
            
            if task in ['detect', 'segment']:
                logs = mongo_record[i]['logs']
                for log in logs:
                    xyn = [(log[k], log[k+1]) for k in range(0, len(log), 2)] # (x, y)
                    xyxyn = poly2xyxy(xyn)
                    
                    results['xyn'].append(xyn)
                    results['xyxyn'].append(xyxyn)
                    results['class_id'].append(class_id)
            else:
                results['class_id'].append(class_id)
            
        suc = True
    
    except Exception as err:
        logging.error(f'Error while extracting annotation: {err}')
        
    return suc, results