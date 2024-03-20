from PIL import Image
from astarMap import get_short_path_by_astar
import numpy as np
import pathlib
from gps_mapping import get_coordinate_gps_mapping
from pre_processing import make_binary_txt_from_image
import os
from pymongo import MongoClient
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


if __name__ == "__main__":
    image_dir = f"{os.getcwd()}/maps"
    binary_dir = f"{os.getcwd()}/binarys"
    pathed_image_dir = f"{os.getcwd()}/pathed_maps"
    path_dir = f"{os.getcwd()}/path"
    union_binary_map_dir=f"{os.getcwd()}/union_binary_map"
    union_map_dir=f"{os.getcwd()}/union_map"
    walkable_spot_dir=f"{os.getcwd()}/walkable_spot"
    gps_matching_dir=f"{os.getcwd()}/gps_matching"
    # preparing folder
    createFolder([binary_dir, pathed_image_dir, path_dir,walkable_spot_dir,union_map_dir,union_binary_map_dir,gps_matching_dir])

    image_list = os.listdir(image_dir)
    binary_image_list = os.listdir(binary_dir)
    pathed_image_list = os.listdir(pathed_image_dir)

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
    
    print("============loading union binary map===========")
    binary_map = np.loadtxt(
        f"{union_binary_map_dir}/union_binary_map.txt", delimiter=" ", dtype="int"
    )
    print(binary_map.shape)
    print("============loaded union binary map===========")

    if not os.path.isfile(f"{union_map_dir}/union_map.png"):
        print("============save start union binary map png===========")
        binary_image = Image.fromarray(binary_map.astype('uint8') * 255, 'L')
        binary_image.save(f"{union_map_dir}/union_map.png",'PNG')
        print("============save end union binary map png end===========")
    
    walkable_spot_tuple = np.where(binary_map == 1)
    walkable_spot_np_list=np.column_stack((walkable_spot_tuple[0],walkable_spot_tuple[1]))
    if not os.path.isfile(f"{walkable_spot_dir}/walable_spot.txt"):
        np.savetxt(f"{walkable_spot_dir}/walable_spot.txt", walkable_spot_np_list, fmt='%d', delimiter=' ')
    walkable_spot_list = [tuple(walkable_spot_np_list[i]) for i in range(walkable_spot_np_list.shape[0])]

    print(f"{len(walkable_spot_list)} walkable spot was detected")

    #start는 월평 가운데쪽
    start= walkable_spot_list[8839096]
    print(start)

    # end= walkable_spot_list[10537581]
    # print(end)

    start_time = time.time()
    path_map,distance=get_short_path_by_dijkstra(binary_map,start)

    # short_path,distance=get_short_path_by_astar(binary_map,start,end)
    end_time = time.time()
    print(f"dj spend time for extract path_map : {end_time - start_time:.5f} sec")

    # if end:
    #     binary_image=Image.fromarray(binary_map.astype('uint8') * 255, 'L').convert("RGB")
    #     print(f"====================save pathed {file_name}===============================")
    #     # 출발점에서 끝점까지 최단경로가 입혀진 이미지를 저장
    #     for x,y in short_path:
    #         binary_image.putpixel((y,x),(200,15,15))
    #     binary_image.save(f"{pathed_image_dir}/{start[0]}_{start[1]}_to_{end[0]}_{end[1]}_pathed_map.png",'PNG')

    print("================get coordinate by gps================")
    gps_mapping_list=get_coordinate_gps_mapping()
    print(len(gps_mapping_list))
    print(len(gps_mapping_list[0]))
    print("================get coordinate by gps ended================")

    print("================tacking path start================")
    start_time = time.time()
    result=dict()
    for end in walkable_spot_list:
        # print(f"=========={start} to {end} path ============")
        if start==end:
            continue
        start_to_end_distance = distance[end[0]][end[1]]
        if start_to_end_distance == INF:
            continue
        short_path = []
        cur_x_y = end
        while cur_x_y != start:
            short_path.append(cur_x_y)
            x, y = cur_x_y
            cur_x_y = path_map[x][y]
        short_path.append(start)
        short_path.reverse()
        (start_lat,start_lon)=gps_mapping_list[start[0]//5][start[1]//5]
        (end_lat,end_long)=gps_mapping_list[end[0]//5][end[1]//5]
        # print(start[0]//5,start[1]//5)
        # print(end[0]//5,end[1]//5)
        # 위도 경도로 저장
        short_path=list(map(lambda point:tuple(gps_mapping_list[point[0]//5][point[1]//5]),short_path))
        exist_set=set()
        insert_short_path=[]
        result[f"{start_lat}_{start_lon}_to_{end_lat}_{end_long}"]=[]
        for point in short_path:
            if point in exist_set:
                continue
            exist_set.add(point)
            insert_short_path.append(point)
        result[f"{start_lat}_{start_lon}_to_{end_lat}_{end_long}"]=insert_short_path
        # print(f"{start} to {end} was taken {len(short_path)} steps and {start_to_end_distance} distance")
    end_time = time.time()
    print("================tacking path end================")
    print(f"spend time for tacking path : {end_time - start_time:.5f} sec")
    with open(f"{path_dir}/{start[0]}_{start[1]}.pkl", 'wb') as f:
        pickle.dump(result, f)

    #     # 목표지점이 주어지지 않았을경우 모든 경로가 저장된 경로배열과 최단거리배열 반환

    #===============================update to db========================================

    # client = MongoClient(
    #     f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
    # )

    # print(client.list_database_names())
    # db = client.dunsan  # 연결 테스트를 위해 admin 데이터베이스 사용
    # dunsanCollection = db.dunsan  # db 에서 collection 을 만든다.

    # short_path, distance = get_short_path_by_astar(binary_map, start, end)

    # post={
    #     "start":start,
    #     "end":end,
    #     "path":short_path
    # }

    # post_id=dunsanCollection.insert_one(post).inserted_id
    # print(dunsanCollection.find_one({"_id": post_id}))
    # print(start,end)