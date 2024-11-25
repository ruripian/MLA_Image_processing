# README: MLA 슈퍼해상도 이미지 처리 파이프라인

  

## 소개  

이 저장소는 MLA(다중 렌즈 배열) 카메라로 촬영한 이미지를 활용해 고해상도 이미지를 생성하는 파이프라인을 제공합니다.  
기본 워크플로우는 이미지 전처리, 중앙 이미지 추출 및 패턴 추출, 패턴 병합 및 선명화로 구성됩니다.  
이 코드를 통해 MLA 이미지를 기반으로 슈퍼 해상도 알고리즘을 구현할 수 있습니다.


---

## 사용법  

### 1. 요구사항  

다음 Python 패키지가 필요합니다.  
필요한 패키지를 설치하려면 아래 명령어를 실행하세요:  

```bash

pip install numpy opencv-python pillow matplotlib

```


### 2. 코드 실행 순서

1. crop_image.py의 `process_image()` 함수를 실행하여 중앙 이미지를 기준으로 전처리된 검출 마스크를 생성합니다.
2. crop_image.py의 `process_and_crop_image()` 함수를 실행하여 중앙 이미지를 기준으로 이미지를 자릅니다.
3. cut_image.py의 `extract_pattern_grid()`를 통해 패턴 그리드를 추출하고 개별 패턴 이미지를 저장합니다.
4. merge_image.py에서 `pattern_out` 폴더에 저장된 이미지를 `tiles`로 병합하고 선명화합니다.

---

## 주요 코드 설명

### crop_image.py
- 입력된 원본 이미지에서 실제 MLA 이미지를 추출합니다.
### cut_image.py
- 추출된 MLA 이미지에서 사용자의 입력과 패턴 정보에 따라 단일 카메라 이미지를 추출합니다.
- 추출하는 이미지의 개수는 9개입니다(3 by 3)
### merge_image

- 9개의 패턴 이미지를 불러와 적절히 정렬한 후 중간값 병합(Median Fusion) 방식을 적용하여 고해상도 이미지를 생성합니다.


---
## 파일 구조
```
├── crop_image.py
├── cut_image.py
├── merge_image.py
├── mla_data/
│   └── Image__...png  # 원본 MLA 이미지
├── pattern_out/
│   └── pattern_1.png ~ pattern_9.png  # 추출된 패턴 이미지
└── output_highres_image.jpg  # 최종 병합 결과물
```

---

## 결과물

최종적으로 생성된 고해상도 이미지는 `output_highres_image.jpg` 파일에 저장됩니다.  
추출된 각 패턴은 `pattern_out/` 폴더에서 확인할 수 있습니다.

---

## 참고

추가 문의 사항이나 오류 보고는 이 저장소의 이슈를 활용해주세요.
