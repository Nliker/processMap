import math

idx_r = 0
idx_c = 0

latlng_map = [[(0, 0)] * 3500 for _ in range(3300)]

def tile_to_latlon(x, y):
    n = 2.0 ** 16
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def read_files(arr):
    global idx_r, idx_c
    i = arr[0]
    j = arr[2]
    
    while(j < arr[3] + 1):
        i = arr[0]
        while (i < arr[1] + 1):
            start_lat, start_lng = tile_to_latlon(i, j)
            mapping_gps(start_lat, start_lng)
            if idx_c == 3500:
                idx_c = 0
                idx_r += 100
                
            i += 1
            
        j += 1
    idx_r=0
    idx_c=0
                
            

def mapping_gps(lat_0, lon_0):
    global idx_r, idx_c
    
    # 조각의 크기
    size = 5  # 미터

    # 위도, 경도 변화량
    delta_lat = size / 112000  # 위도 1도는 대략 111~ 112km
    delta_lon = size / (112000 * math.cos(math.radians(lat_0)))  # 경도 1도는 위도에 따라 변함

    tmp_r = idx_r
    tmp_c = idx_c
    #지도 조각안의 숫자들(0 or 1)을 5m x 5m로 묶은 좌표
    for i in range(100):
        for j in range(100):
            lat = lat_0 - delta_lat * i
            lon = lon_0 + delta_lon * j
            latlng_map[tmp_r][tmp_c + j] = (lat, lon)
            
            if tmp_r == 3299:
                # print(tmp_r, tmp_c+j)
                ...
            
        tmp_r += 1
        if i == 99:
            idx_c += 100
            if j == 99:
                tmp_r = idx_r
        else:
            tmp_c = idx_c


def get_coordinate_gps_mapping():
    x_min = 55941
    y_min = 25643
    x_max = 55975
    y_max = 25675
    
    arr = [x_min, x_max, y_min, y_max]
    read_files(arr)
    return latlng_map
