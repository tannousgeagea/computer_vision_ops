from augmentation.usecases.by_images import augment_data_by_image


mode_map = {
    'by-images': augment_data_by_image.augment,
}


def main(mode):
    assert mode in mode_map.keys(), f"Unsupported mode. expected one of {list(mode_map.keys())}, got {mode}"
    
    augment =  mode_map[mode]
    augment()

if __name__ == '__main__':
    main(mode='by-images')
    
     