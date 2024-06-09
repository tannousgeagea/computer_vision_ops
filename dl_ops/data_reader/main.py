import os
from datetime import date
from utils.config import data_acquisition_mode
from data_reader.usecases.from_server import fetch_images_from_server
from data_reader.usecases.from_local import fetch_images_from_local
from data_reader.usecases.from_mongo import fetch_images_info_from_mongo


mode_map = {
    'from-server': fetch_images_from_server.serve,
    'from-local': fetch_images_from_local.serve,
    'from-mongo':fetch_images_info_from_mongo.serve
}


def main(mode = 'from-server'):
    assert mode in mode_map.keys(), f"Unsupported Fetching mode. expteced one of {list(mode_map.keys())}, got {mode}"
    
    serve = mode_map[mode]
    serve()
    
if __name__ == "__main__":
    print(f"Acquiring data mode: {data_acquisition_mode}")
    main(mode = data_acquisition_mode)