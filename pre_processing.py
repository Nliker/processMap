from PIL import Image
import numpy as np

def make_binary_txt_from_image(image_name : str,image_dir : str,save_name : str,save_dir : str):
    print("-----------------image to binary starting-----------------")
    # 이미지를 불러옴
    img = Image.open(f"{image_dir}/{image_name}")  # 이미지 경로 수정
    print(f"Load image: {image_name}")
    # 이미지가 RGB 모드인지 확인 후, 아니라면 변환
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # # 이미지의 크기를 500x500으로 조정
    # if(img.size != (500,500)):
    #     img = img.resize((500, 500), Image.Resampling.LANCZOS) 
    # img.save("test.png")
    # 컬러 이미지를 배열로 변환
    img_array = np.array(img)

    # 특정 RGB 값을 정의 -> 흰색 = 길
    # target_colors = [[249, 249, 249], [255, 255, 255]]
    target_color = [[255, 255, 255]]
    # 여러 타겟 색상에 대한 이진 배열을 초기화
    binary_array = np.zeros(img_array.shape[:2], dtype=int)
    # print(np.all(img_array == target_color, axis=-1))
    # 각 타겟 색상에 대해 이진 배열을 업데이트
    binary_array = np.logical_or(binary_array, np.all(img_array == target_color, axis=-1)).astype(int)
    # print(binary_array)
    # binary_array 데이터를 텍스트 파일로 저장
    np.savetxt(f"{save_dir}/{save_name}", binary_array, fmt='%d', delimiter=' ')
    print(f"saved binaryed image: {save_name}")
    print("-----------------image to binary end-----------------")
    # # 이진 배열로부터 이미지 생성
    # binary_image = Image.fromarray(binary_array.astype('uint8') * 255, 'L')
    # # 이미지를 저장
    # binary_image.save(save_path)
