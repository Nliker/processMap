from PIL import Image
from astarMap import get_shortest_path
import numpy as np
from pathImg import get_pathed_image
from pre_processing import make_binary_txt_from_image
import os
from pymongo import MongoClient

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
    client = MongoClient(
        f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"
    )

    print(client.list_database_names())
    db = client.walkable_spots  # 연결 테스트를 위해 admin 데이터베이스 사용
    dunsanCollection = db.dunsan  # db 에서 collection 을 만든다.
    image_dir = f"{os.getcwd()}/maps"
    binary_dir = f"{os.getcwd()}/binarys"
    pathed_image_dir = f"{os.getcwd()}/pathed_maps"
    path_dir = f"{os.getcwd()}/path"

    # preparing folder
    createFolder([binary_dir, pathed_image_dir, path_dir])

    image_list = os.listdir(image_dir)
    binary_image_list = os.listdir(binary_dir)
    pathed_image_list = os.listdir(pathed_image_dir)

    for file_name in [file for file in image_list if file.endswith(".png")]:
        print(
            f"=======================process {file_name}==============================="
        )

        binary_name = os.path.splitext(file_name)[0] + ".txt"
        if binary_name not in binary_image_list:
            make_binary_txt_from_image(file_name, image_dir, binary_name, binary_dir)

        binary_map = np.loadtxt(
            f"{binary_dir}/{binary_name}", delimiter=" ", dtype="int"
        )
        walkable_spot_tuple = np.where(binary_map == 1)

        walkable_spot_list = [
            (walkable_spot_tuple[0][i], walkable_spot_tuple[1][i])
            for i in range(len(walkable_spot_tuple[0]))
        ]

        print(f"{len(walkable_spot_list)} walkable spot was detected")

        start = walkable_spot_list[1000]
        end = walkable_spot_list[500000]
        print(binary_map[start[0]][start[1]])
        print(binary_map[end[0]][end[1]])
        # for start in walkable_spot_list:
        #     for end in walkable_spot_list:
        #         if start==end:
        #             continue
        #         short_path,distance=get_shortest_path(binary_map,start,end)

        #         img = Image.open(f"{image_dir}/{file_name}")  # 이미지 경로 수정
        #         # 이미지가 RGB 모드인지 확인 후, 아니라면 변환
        #         if img.mode != 'RGB':
        #             img = img.convert('RGB')
        #         img_array = np.array(img)

        #         pathed_img_array=get_pathed_image(img_array,short_path)
        #         pathed_img = Image.fromarray(pathed_img_array)
        #         print(f"====================save pathed {file_name}===============================")
        #         # 이미지를 저장
        #         pathed_img.save(f"{pathed_image_dir}/{file_name}")
        short_path, distance = get_shortest_path(binary_map, start, end)
        print(distance)
        img = Image.open(f"{image_dir}/{file_name}")  # 이미지 경로 수정
        # 이미지가 RGB 모드인지 확인 후, 아니라면 변환
        if img.mode != "RGB":
            img = img.convert("RGB")
        img_array = np.array(img)

        pathed_img_array = get_pathed_image(img_array, short_path)
        pathed_img = Image.fromarray(pathed_img_array)
        print(
            f"====================save pathed {file_name}==============================="
        )
        # 이미지를 저장
        pathed_img.save(f"{pathed_image_dir}/{file_name}")
