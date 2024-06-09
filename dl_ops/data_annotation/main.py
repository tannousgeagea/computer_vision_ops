
from utils.config import data_annotation_mode
from data_annotation.usecases.from_mongo import read_annotation_from_mongo

mode_map = {
    'from-mongo': read_annotation_from_mongo.annotate,
}

def main(mode):
    assert mode in mode_map.keys(), f"Unsupported mode. expected one of {list(mode_map.keys())}, got {mode}"
    
    annotate = mode_map[mode]
    annotate()
    
if __name__ == "__main__":
    main(mode=data_annotation_mode)