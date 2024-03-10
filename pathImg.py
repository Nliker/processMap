from PIL import Image

rgb_red=[200,15,15]

def get_pathed_image(img_array : list[list[int]],path : list[int])->Image:
    for x,y in path:
        img_array[x][y]=rgb_red
    return img_array

