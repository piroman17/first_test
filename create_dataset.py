import cv2
import json
import os
from tqdm import tqdm

os.makedirs('with_mask', exist_ok=True)
os.makedirs('without_mask', exist_ok=True)

images = os.listdir('C:/Users/kutak/Medical_mask/Medical Mask/images')

cls = {'face_with_mask': 0, 'face_with_mask_incorrect': 0, 'face_no_mask': 0, 'face_other_covering': 0}

for img_name in tqdm(images):
    img = cv2.imread(f'C:/Users/kutak/Medical_mask/Medical Mask/images/{img_name}', cv2.IMREAD_GRAYSCALE)
    with open(f'C:/Users/kutak/Medical_mask/Medical Mask/annotations/{img_name}.json', 'r') as f:
        a = json.load(f)
    for obj in a['Annotations']:
        if obj['classname'] in cls:
            cls[obj['classname']] += 1
            x1, y1, x2, y2 = obj['BoundingBox']
            face = img[y1: y2, x1: x2]
            if obj['classname'] in ['face_other_covering', 'face_no_mask']:
                cv2.imwrite(f'without_mask/cover_{cls[obj["classname"]]}.png', face)
            elif obj['classname'] == 'face_with_mask':
                cv2.imwrite(f'with_mask/cover_{cls[obj["classname"]]}.png', face)
print(cls)
