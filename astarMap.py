import math
import numpy as np
import heapq

x_offset = [0, 0, 1, -1, 1, 1, -1, -1]
y_offset = [1, -1, 0, 0, 1, -1, 1, -1]
INF = 1e8


# https://meticulousdev.tistory.com/entry/PYTHON-%ED%83%80%EC%9E%85-%ED%9E%8C%ED%8A%B8%EC%97%90%EC%84%9C-List%EC%99%80-list%EC%9D%98-%EC%B0%A8%EC%9D%B4
def get_short_path_by_astar(
    map: list[list[int]], start: tuple, end: tuple
) -> tuple[list, float]:
    print("========ready for variables==========")
    h = len(map)
    w = len(map[0])
    heuristic_cost = [[INF] * w for _ in range(h)]
    total_cost_list = [[INF] * w for _ in range(h)]
    path_map = [[[0, 0]] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if map[i][j]:
                heuristic_cost[i][j] = round(get_euclidean_distance((i, j), end), 3)
    print("========ready for variables end==========")
    heap = []
    total_cost = 0
    heapq.heappush(
        heap, (heuristic_cost[start[0]][start[1]] + total_cost, start[0], start[1])
    )
    cnt = 1
    while heap and (heap[0][1:]) != end:
        total_cost, x, y = heapq.heappop(heap)
        # Total Cost 에서 휴리스틱 코스트를 빼면 시작 지점에서 현재 지점까지의 실제 거리를 구할 수 있음
        if (
            total_cost_list[x][y] < total_cost
        ):  # 기존에 있는 거리보다 길다면, 볼 필요도 없음
            continue
        depth = total_cost - heuristic_cost[x][y]
        # 유효한 인접 노드가 있으면 코스트를 계산해 힙에 넣는다.
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt)
        for i in range(8):
            nx = x + x_offset[i]
            ny = y + y_offset[i]
            next_distance = depth + ((nx - x) ** 2 + (ny - y) ** 2) ** (1 / 2)
            if is_vaild(map, nx, ny):
                if (next_distance + heuristic_cost[nx][ny]) < total_cost_list[nx][ny]:
                    total_cost = next_distance + heuristic_cost[nx][ny]
                    total_cost_list[nx][ny] = total_cost
                    path_map[nx][ny] = (x, y)
                    heapq.heappush(heap, (total_cost, nx, ny))
    distance = total_cost_list[end[0]][end[1]] - heuristic_cost[end[0]][end[1]]
    short_path = []
    if distance == INF:
        return (short_path, distance)
    cur_x_y = end
    while cur_x_y != start:
        short_path.append(cur_x_y)
        x, y = cur_x_y
        cur_x_y = path_map[x][y]
    short_path.append(start)
    return (short_path, distance)


def get_euclidean_distance(pq1: int, pq2: int):
    p1, q1 = pq1
    p2, q2 = pq2

    return math.sqrt((p1 - p2) ** 2 + (q1 - q2) ** 2)


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
