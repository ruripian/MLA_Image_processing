import os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

output_dir = "pattern_out"
tiles = []

for filename in sorted(os.listdir(output_dir)):
    if filename.endswith(".png"):
        base_name = os.path.splitext(filename)[0]  
        if base_name[-1] in '0123456789':
            tile = Image.open(os.path.join(output_dir, filename))
            tiles.append((base_name, tile))

if not tiles:
    print("No tiles found in the specified folder. Please check the files.")
else:
    
    tile_width, tile_height = tiles[0][1].size

    stacked_images = np.zeros((len(tiles), tile_height, tile_width, 3), dtype=np.uint8)

    for idx, (base_name, tile) in enumerate(tiles):
        tile_array = np.array(tile, dtype=np.uint8)
        
        if base_name[-1] == '1' or base_name[-1] == '4' or base_name[-1] == '7':  # '1', '4', '7'로 끝나는 경우
            tile_array = np.roll(tile_array, 0, axis=1) 
        elif base_name[-1] == '3' or base_name[-1] == '6' or base_name[-1] == '9':  # '3', '6', '9'로 끝나는 경우
            tile_array = np.roll(tile_array, 0, axis=1)
        
        # 배열에 저장
        stacked_images[idx] = tile_array

    # 중간값 계산
    final_image_array = np.median(stacked_images, axis=0).astype(np.uint8)

    final_image = Image.fromarray(final_image_array)

    unsharp_image = final_image.filter(ImageFilter.UnsharpMask(radius=2, percent=110, threshold=3))

    # 최종 결과 이미지 저장 및 표시
    unsharp_image.save("output_highres_image.jpg")
