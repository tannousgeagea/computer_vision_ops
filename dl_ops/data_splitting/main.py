from utils.config import data_splitting_mode
from data_splitting.usecases.by_images import split_data_by_images
from data_splitting.usecases.by_classes import split_data_by_classes


mode_map = {
    'by-images': split_data_by_images.train_val_split,
    'by-classes': split_data_by_classes.train_val_split,
}

def main(mode):
    assert mode in mode_map.keys(), f"Unsupported mode. expected one of {list(mode_map.keys())}, got {mode}"
    
    train_val_split = mode_map[mode]
    train_val_split()
    
if __name__ == "__main__":
    
    print(data_splitting_mode)
    main(mode=data_splitting_mode)