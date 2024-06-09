from data_reader.splitting.usecases.by_classes import splid_data_by_classes
from data_reader.splitting.usecases.by_images import split_data_by_images

mode_map = {
    'by-classes': splid_data_by_classes.train_val_split,
    'by-images': split_data_by_images.train_val_split,
}


def main(mode):
    assert mode in mode_map.keys(), f"Unsupported mode. expected one of {list(mode_map.keys())}, got {mode}"
    
    train_val_split =  mode_map[mode]
    train_val_split()

if __name__ == '__main__':
    main(mode='by-images')