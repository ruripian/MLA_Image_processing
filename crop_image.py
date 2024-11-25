import cv2
import numpy as np

def process_image(image_path):
    image = cv2.imread(image_path)

    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    hsv_image = cv2.cvtColor(denoised_image, cv2.COLOR_RGB2HSV)

    # 색상 필터 범위 설정 (검은색 영역)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])  

    mask = cv2.inRange(hsv_image, lower_black, upper_black)

    black_regions = cv2.bitwise_and(denoised_image, denoised_image, mask=mask)

    black_only = np.zeros_like(black_regions)
    black_only[np.all(black_regions == [0, 0, 0], axis=-1)] = [255, 255, 255]
    label_data = 255 - black_only


    label_data_gray = cv2.cvtColor(label_data, cv2.COLOR_RGB2GRAY)

    _, binary = cv2.threshold(label_data_gray, 127, 255, cv2.THRESH_BINARY_INV)  

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    height, width = binary.shape
    center = (width // 2, height // 2)

    valid_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w >= 50 and h >= 50:  # 최소 크기 조건 확인
            valid_contours.append(contour)

    closest_contour = None
    min_distance = float('inf')
    for contour in valid_contours:

        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            distance = np.sqrt((cx - center[0])**2 + (cy - center[1])**2)
            if distance < min_distance:
                min_distance = distance
                closest_contour = contour

    result = np.zeros_like(binary)
    if closest_contour is not None:
        cv2.drawContours(result, [closest_contour], -1, (255), thickness=cv2.FILLED)
    
    return result


def sort_points(pts):
    """ 점들을 왼쪽 위, 오른쪽 위, 오른쪽 아래, 왼쪽 아래로 정렬 """
    # 점들을 정렬하기 위해 평균 x, y 좌표 계산
    center = np.mean(pts, axis=0)
    sorted_pts = sorted(pts, key=lambda p: np.arctan2(p[1] - center[1], p[0] - center[0]))
    return np.array(sorted_pts, dtype="float32")

def process_and_crop_image(image,original_image_path):
    original_image = cv2.imread(original_image_path)

    _, binary_mask = cv2.threshold(image, 240, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        #컨투어 정렬
        largest_contour = max(contours, key=cv2.contourArea)
        
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)  
        box = np.int0(box)
        sorted_box = sort_points(box)

        src_pts = sorted_box
        dst_pts = np.array([[0, 0], [rect[1][0] - 1, 0], [rect[1][0] - 1, rect[1][1] - 1], [0, rect[1][1] - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        cropped_image = cv2.warpPerspective(original_image, M, (int(rect[1][0]), int(rect[1][1])))

        return cropped_image
    else:
        print("No contours found.")

# 사용 예시
black_image = process_image("mla_data/Image__2024-06-10__22-26-58.png")
processed_image = process_and_crop_image(black_image,"mla_data/Image__2024-06-10__22-26-58.png")
cv2.imwrite("cropped_image.png", processed_image)
