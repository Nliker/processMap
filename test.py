import pickle
import os
import math
import time

from gps_mapping import get_coordinate_gps_mapping



# path_dir = f"{os.getcwd()}/path"
# with open(f'{path_dir}/6104_8741.pkl', 'rb') as f:
#     data = pickle.load(f)

# # print(len(data.keys()))
# # print(data)
# temp_list=[]
# temp=set()
# for key,val in data.items():
#     if 400>len(val)>300:
#         print(key)
#         print(list(map(lambda x : list(x),data[key])))
#         break


# gps_matching_dir=f"{os.getcwd()}/gps_matching"


def binary_search(numbers, key):
    left = 0
    right = len(numbers)-1
    while left <= right:
        mid = (left + right) // 2
        if key == numbers[mid]:
            return numbers[mid]
        elif key < numbers[mid]:
            right = mid - 1
        elif key > numbers[mid]:
            left = mid + 1
    if right == -1:
        return numbers[0]
    elif left == len(numbers):
        return numbers[-1]
    else:
        right_number = numbers[left]
        left_number = numbers[right]
            
        right_abs = abs(key - right_number)
        left_abs = abs(key - left_number)
        if right_abs == left_abs:
            return right_number
        elif right_abs > left_abs: # next is closer
            return left_number
        elif right_abs < left_abs:
            return right_number

def lat_lon_array_binary_search(test_list,key):
    print(key)

    #x=>행(위도)
    #y=>열(경도)
    x_up=0
    x_down=len(test_list)-1
    y_left=0
    y_right=len(test_list[0])-1
    # 찾는 key가 무조건 존재한다는 가정하에 조건을 분기
    while( x_up<=x_down and y_left<=y_right):
        x_mid=(x_up+x_down)//2
        y_mid=(y_left+y_right)//2
        cur_key=test_list[x_mid][y_mid]
        # print(f"x_up: {x_up} , x_down: {x_down}, y_left: {y_left} , y_right: {y_right}")
        # print(x_mid,y_mid)
        if key==cur_key:
            # 찾는 값과 일치한다면 바로 반환
            return (x_mid,y_mid)
        
        elif key[0]==cur_key[0]:
            # 위도가 같다면 위도의 범위를 한개로 좁힘
            x_up=x_mid
            x_down=x_mid

            if key[1]<cur_key[1]:
                # 경도가 더 작다면 경도의 범위를 왼쪽으로 좁힘
                y_right=y_mid-1

            elif key[1]>cur_key[1]:
                # 경도가 더 크다면 경도의 범위를 오른쪽으로 좁힘
                y_left=y_mid+1

        elif key[0]<cur_key[0]:
            # 위도가 더 작다면 위도의 범위를 아래로 좁힘 
            x_up=x_mid+1

            if key[1]>cur_key[1]:
                # 경도가 더 크다면 경도의 범위를 오른쪽으로 좁힘
                y_left=y_mid+1
            elif key[1]==cur_key[1]:
                # 경도가 같았다면 경도의 범위를 기준포함 오른쪽으로 좁힘
                y_left=y_mid

        elif key[0]>cur_key[0]:
            # 위도가 더 크다면 위도의 범위를 위로 좁힘
            x_down=x_mid-1
        
            if key[1]<cur_key[1]:
                # 경도가 더 작다면 경도의 범위를 왼쪽으로 좁힘
                y_right=y_mid-1
            elif key[1]==cur_key[1]:
                # 경도가 같다면 경도의 범위를 기준 포함 왼쪽으로 좁힘
                y_right=y_mid

    if x_down==-1:
        if y_right==-1:
            return (0,0)
    return f"x_up: {x_up} , x_down: {x_down}, y_left: {y_left} , y_right: {y_right}"
    #     elif y_left<=y_right:
    #         return ("이진탐색")
    # elif x_up==4:
    #     if y_left==4: 
    #         #key가 오른쪽 위로 벗어날 때
    #         return ("========",test_list[len(test_list)-1][len(test_list[0])-1])
    #     elif y_left<=y_right:
    #         return ("이진탐색")
    # elif x_up>x_down: #x가 존재하지 않는 성분일 때(어긋났을 때)
    #     if y_left<=y_right: #y가 정상 범주일 때
    #         #y_right의 왼쪽으로 비교
    #         pass
    # elif x_up==x_down: #x가 존재하는 성분일때
    #     pass

    return f"x_up: {x_up} , x_down: {x_down}, y_left: {y_left} , y_right: {y_right}"
print("================get coordinate by gps================")
gps_mapping_list=get_coordinate_gps_mapping()
print("================get coordinate by gps ended================")
# start = time.time()
# test_input=(36.26200168858323, 127.48533995537568)
# min_distance=math.dist(gps_mapping_list[0][0],test_input)
# min_distance_index=(0,0)
# for i in range(len(gps_mapping_list)):
#     for j in range(len(gps_mapping_list[0])):
#         cur_distance=math.dist(gps_mapping_list[i][j],test_input)
#         if min_distance>cur_distance:
#             min_distance=cur_distance
#             min_distance_index=(i,j)
# end = time.time()
# print(f"{end - start:.5f} sec")
# print(min_distance)
# print(min_distance_index)

# print(gps_mapping_list[0][1000])
# print(gps_mapping_list[1000][1000])
# print(gps_mapping_list[2000][1000])
# print(gps_mapping_list[3000][1000])


# print("=======================")
# print(gps_mapping_list[0][1004])
# print(gps_mapping_list[1000][1004])
# print(gps_mapping_list[2000][1004])
# print(gps_mapping_list[3000][1004])

# def binary_search(numbers, key):
#     left = 0
#     right = len(numbers)-1
#     while left <= right:
#         mid = (left + right) // 2
#         if key == numbers[mid]:
#             return numbers[mid]
#         elif key < numbers[mid]:
#             right = mid - 1
#         elif key > numbers[mid]:
#             left = mid + 1
#     return -1

# print("=============key가 리스트중에 있는 경우==============")
# print(f"list: {[10,20,30,40]}, key: {20}, nearest key: {binary_search([10,20,30,40],20)}")
# print("=============key가 리스트의 가장 작은 수보다 작은 경우==============")
# print(f"list: {[10,20,30,40]}, key: {5}, nearest key: {binary_search([10,20,30,40],5)}")
# print("=============key가 리스트의 가장 큰 수보다 큰 경우==============")
# print(f"list: {[10,20,30,40]}, key: {45}, nearest key: {binary_search([10,20,30,40],45)}")
# print("=============key가 리스트의 가장 작은 수와 가장 큰 수 사이에 있을 경우==============")
# print(f"list: {[10,20,30,40]}, key: {33}, nearest key: {binary_search([10,20,30,40],33)}")

test_list=[
            [
                [8,20],[8,25],[8,30],[8,35]
            ],
            [
                [6,15],[6,20],[6,25],[6,35]
            ],
            [
                [4,15],[4,20],[4,25],[4,35]
            ],
            [
                [2,10],[2,15],[2,25],[2,30]
            ]
        ]


print("=================x가 어긋났고 범위 밖에 있을때")
print(lat_lon_array_binary_search(test_list,[50,0]))
print(lat_lon_array_binary_search(test_list,[0,0]))
print(lat_lon_array_binary_search(test_list,[0,100]))
print(lat_lon_array_binary_search(test_list,[100,26]))

# print("=================x가 어긋났고 범위 안에 있을때")
# print(lat_lon_array_binary_search(test_list,[3,9]))
# print(lat_lon_array_binary_search(test_list,[3,10]))
# print(lat_lon_array_binary_search(test_list,[3,11]))
# print(lat_lon_array_binary_search(test_list,[3,14]))
# print(lat_lon_array_binary_search(test_list,[3,15]))
# print(lat_lon_array_binary_search(test_list,[3,19]))
# print(lat_lon_array_binary_search(test_list,[3,20]))
# print(lat_lon_array_binary_search(test_list,[3,25]))
# print(lat_lon_array_binary_search(test_list,[4,26]))