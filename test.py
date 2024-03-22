import pickle
import os
import math
import time
import numpy as np
from convert import lat_lon_array_binary_search
from djMap import get_nearest_walkable_spot
from prepare_maps import get_binary_map, get_coordinate_gps_mapping, get_shelter_index
        
if __name__ == "__main__":
    shelter_dir = f"{os.getcwd()}/shelter_index"

    gps_mapping_list=get_coordinate_gps_mapping()
    binary_map=get_binary_map()
    result=dict()
    with open(f"{shelter_dir}/shelters.pkl", 'rb') as f:
        shelter_data = pickle.load(f)
        for key,val in shelter_data.items():
            shelter_id=key
            [shelter_lat,shelter_lon]=val
            start= lat_lon_array_binary_search(gps_mapping_list,(shelter_lat,shelter_lon))
            start=(start[0]*5,start[1]*5)
            walkable_start=get_nearest_walkable_spot(binary_map,start)
            
            insert_dict={
                "lat":shelter_lat,
                "lon":shelter_lon,
                "walkable_start":walkable_start
            }
            result[shelter_id]=insert_dict
    with open(f"{shelter_dir}/shelter_index.pkl", 'wb') as f:
        pickle.dump(result, f)