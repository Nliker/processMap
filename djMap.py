
import heapq
from PIL import Image
import os
import numpy as np
import math


x_offset=[0,0,1,-1,1,1,-1,-1]
y_offset=[1,-1,0,0,1,-1,1,-1]
INF = 1e8

def get_short_path_by_dijkstra(map :list[list[int]],start:tuple):
    print("========ready for variables==========")
    w=len(map[0])
    h=len(map)
    map[start[0]][start[1]]=2
    distance=[[INF] * w for _ in range(h)]
    path_map = [[[0, 0]] * w for _ in range(h)]
    print("========ready for variables end==========")

    # walkable_sport_dir=f"{os.getcwd()}/batch_area_images"
    # binary_image = Image.fromarray(map.astype('uint8') * 255, 'L').convert("RGB")
    # print(binary_image.size)

    heap = []
    heapq.heappush(heap,(0,*start))
    distance[start[0]][start[1]]=0
    # binary_image.putpixel((start[1],start[0]),(200,15,15)) 
    
    cnt = 0
    while heap:
        dist,x,y=heapq.heappop(heap)

        cnt += 1
        if cnt % 100000 == 0:
            print(cnt)
            # binary_image.save(f"{walkable_sport_dir}/{start[0]}_{start[1]}_{cnt}.png",'PNG')

        if distance[x][y] < dist:
            continue

        for i in range(8):
            nx=x_offset[i]+x
            ny=y_offset[i]+y
            if not is_vaild(map, nx, ny) or (math.dist(start,[nx,ny])>=3000):
                continue

            next_distance=((nx-x)**2+(ny-y)**2)**(1/2)+dist
            if next_distance<distance[nx][ny]:
                distance[nx][ny]=next_distance
                path_map[nx][ny] = (x, y)
                # binary_image.putpixel((ny,nx),(200,15,15))
                heapq.heappush(heap,(next_distance,nx,ny))
    return path_map,distance
    # print("==========start end path finding============")
    # 목표지점을 줬을 경우 목표지점까지의 최단경로,거리를 반환
    # if end:
    #     if start==end:
    #         return [],0
    #     start_to_end_distance = distance[end[0]][end[1]]
    #     if start_to_end_distance == INF:
    #         return [],0
    #     short_path = []
    #     cur_x_y = end
    #     while cur_x_y != start:
    #         short_path.append(cur_x_y)
    #         x, y = cur_x_y
    #         cur_x_y = path_map[x][y]
    #     short_path.append(start)
    #     print(f"{start} to {end} was taken {len(short_path)} steps and {start_to_end_distance} distance")
    #     print("==========start end path finding end============")
    #     return (short_path,start_to_end_distance)
    # else:
    #     # 목표지점이 주어지지 않았을경우 모든 경로가 저장된 경로배열과 최단거리배열 반환
    #     for end in walkable_spot_list:
    #         print(f"=========={start} to {end} finding============")
    #         if start==end:
    #             continue
    #         start_to_end_distance = distance[end[0]][end[1]]
    #         if start_to_end_distance == INF:
    #             continue
    #         short_path = []
    #         cur_x_y = end
    #         while cur_x_y != start:
    #             short_path.append(cur_x_y)
    #             x, y = cur_x_y
    #             cur_x_y = path_map[x][y]
    #         short_path.append(start)
    #         print(f"{start} to {end} was taken {len(short_path)} steps and {start_to_end_distance} distance")
    #     print("==========start end path finding end============")
    #     return (path_map,distance)


def is_vaild(map: list[list[int]], row: int, col: int):
    h = len(map)
    w = len(map[0])

    # out of bound 처리
    if not (0 <= row < h and 0 <= col < w):
        return False

    # 유효하지 않은 노드 처리
    if map[row][col] == 0:
        return False

    return True