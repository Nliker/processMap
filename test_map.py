import numpy as np
import pathlib
from prepare_maps import get_binary_map, get_coordinate_gps_mapping, get_shelter_index
from pre_processing import make_binary_txt_from_image
import os
from djMap import get_short_path_by_dijkstra
import time
import pickle

mongo_host = "localhost"  # 또는 컨테이너의 IP 주소
mongo_port = 27017
mongo_user = "ssafy"
mongo_password = "ssafy"

INF = 1e8

def createFolder(directorys: list):
    try:
        for directory in directorys:
            if not os.path.exists(directory):
                os.makedirs(directory)
    except OSError:
        print("Error: Creating directory. " + directory)

image_dir = f"{os.getcwd()}/maps"
binary_dir = f"{os.getcwd()}/binarys"
path_dir = f"{os.getcwd()}/path"
union_binary_map_dir=f"{os.getcwd()}/union_binary_map"
walkable_spot_dir=f"{os.getcwd()}/walkable_spot"

def make_short_path(binary_map,gps_mapping_list,walkable_spot_np_list,shelter_id,start):
    start_time = time.time()
    path_map,distance=get_short_path_by_dijkstra(binary_map,start)

    end_time = time.time()
    print(f"dj spend time for extract path_map : {end_time - start_time:.5f} sec")

    print(f"================{start} tacking path start================")
    start_time = time.time()
    result=dict()
    for end in walkable_spot_np_list:
        if (start==end).all():
            continue
        start_to_end_distance = distance[end[0]][end[1]].item()
        if start_to_end_distance == INF:
            continue
        short_path = []
        cur_x_y = end
        while not (start==cur_x_y).all():
            short_path.append(cur_x_y)
            x, y = cur_x_y
            cur_x_y = path_map[x][y]
        short_path.append(start)
        (end_lat,end_long)=gps_mapping_list[end[0]//5][end[1]//5]

        # 위도 경도로 저장
        short_path=list(map(lambda point:tuple(gps_mapping_list[point[0]//5][point[1]//5]),short_path))
        exist_set=set()
        insert_short_path=[]
        for point in short_path:
            if point in exist_set:
                continue
            exist_set.add(point)
            insert_short_path.append(point)

        result[f"{end_lat}_{end_long}_to_{shelter_id}"]={
            "path":insert_short_path,
            "distance":start_to_end_distance
        }
    end_time = time.time()
    print("================tacking path end================")
    print(f"spend time for tacking path : {end_time - start_time:.5f} sec")

    with open(f"path_dir/{shelter_id}.pkl", 'wb') as f:
        pickle.dump(result, f)

if __name__ == "__main__":
    # preparing folder
    createFolder([binary_dir, path_dir,walkable_spot_dir,union_binary_map_dir])
    image_list = os.listdir(image_dir)
    binary_image_list = os.listdir(binary_dir)

    image_png_list=[file for file in image_list if file.endswith(".png")]
    
    for file_name in image_png_list:
        print(
            f"=======================make_binary_txt_from_image {file_name}==============================="
        )
        binary_name = os.path.splitext(file_name)[0] + ".txt"
        if binary_name not in binary_image_list:
            make_binary_txt_from_image(file_name, image_dir, binary_name, binary_dir)
        print(
            f"=======================make_binary_txt_from_image {file_name} done==============================="
        )

    #map들에 대한 이진맵이 없다면 이진맵을 준비합니다.
    if not os.path.isfile(f"{union_binary_map_dir}/union_binary_map.txt"):
        splited_file_name=list(map(lambda file_name:list(map(int,pathlib.Path(file_name).stem.split("_"))),image_png_list))

        splited_file_name.sort(key=lambda x:(x[1],x[0]))

        splited_file_name=list(map(lambda x:str(x[0])+"_"+str(x[1])+".txt",splited_file_name))

        reshaped_file_name_list=np.array(splited_file_name).reshape(33,35)    

        union_binary_map=np.array([])

        for line_numpy_binary_map in reshaped_file_name_list:
            line_binary_map_stack=np.array([])

            for file_name in line_numpy_binary_map:
                binary_map = np.loadtxt(
                    f"{binary_dir}/{file_name}", delimiter=" ", dtype="int"
                )   
                if line_binary_map_stack.size==0:
                    line_binary_map_stack=binary_map
                else:
                    line_binary_map_stack=np.concatenate([line_binary_map_stack,binary_map],axis=1)
            print(line_binary_map_stack.shape)
            if union_binary_map.size==0:
                union_binary_map=line_binary_map_stack
            else:
                union_binary_map=np.concatenate((union_binary_map,line_binary_map_stack),axis=0)
            print(union_binary_map.shape)
        np.savetxt(f"{union_binary_map_dir}/union_binary_map.txt", union_binary_map, fmt='%d', delimiter=' ')
        print("============saved union binary map===========")

    binary_map=get_binary_map()
    walkable_spot_tuple = np.where(binary_map == 1)
    walkable_spot_np_list=np.column_stack((walkable_spot_tuple[0],walkable_spot_tuple[1]))

    #갈수 있는 모든 지점들을 준비합니다.
    if not os.path.isfile(f"{walkable_spot_dir}/walable_spot.txt"):
        np.savetxt(f"{walkable_spot_dir}/walable_spot.txt", walkable_spot_np_list, fmt='%d', delimiter=' ')

    print(f"{walkable_spot_np_list.shape[0]} walkable spot was detected")

    gps_mapping_list=get_coordinate_gps_mapping()
    shelter_dict=get_shelter_index()

    
    shelter_id="65fd1f64a1c2102da599d059"
    shelter_info=shelter_dict[shelter_id]
    print(shelter_info)

    make_short_path(binary_map,gps_mapping_list,walkable_spot_np_list,shelter_id,shelter_info["walkable_start"])