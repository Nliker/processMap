from PIL import Image
from astarMap import get_short_path_by_astar
import numpy as np
import pathlib
from pathImg import get_pathed_image
from pre_processing import make_binary_txt_from_image
import os
from pymongo import MongoClient
from djMap import get_short_path_by_dijkstra
import time

mongo_host = "localhost"  # 또는 컨테이너의 IP 주소
mongo_port = 27017
mongo_user = "ssafy"
mongo_password = "ssafy"


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
    # preparing folder
    createFolder([binary_dir, pathed_image_dir, path_dir])

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
    end= walkable_spot_list[10537581]
    print(end)

    start_time = time.time()
    short_path,distance=get_short_path_by_dijkstra(binary_map,start,walkable_spot_list,end)
    # short_path,distance=get_short_path_by_astar(binary_map,start,end)
    end_time = time.time()
    print(f"{end_time - start_time:.5f} sec")
    print(distance)
    if end:
        binary_image=Image.fromarray(binary_map.astype('uint8') * 255, 'L').convert("RGB")
        print(f"====================save pathed {file_name}===============================")
        # 출발점에서 끝점까지 최단경로가 입혀진 이미지를 저장
        for x,y in short_path:
            binary_image.putpixel((y,x),(200,15,15))
        binary_image.save(f"{pathed_image_dir}/{start[0]}_{start[1]}_to_{end[0]}_{end[1]}_pathed_map.png",'PNG')

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