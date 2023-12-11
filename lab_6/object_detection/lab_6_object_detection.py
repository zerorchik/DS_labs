import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
from ultralytics import YOLO

# Зававантаження попередньо навченої моделі
model = YOLO('yolov8n.pt')

# Донавчання моделі
results = model.train(data='coco128.yaml', epochs=3)

# Оцінка продуктивності моделі на валідаційному наборі
results = model.val()

# Тестування на відео та збереження моделі
results = model.track(source='V_6.mp4', show=True, tracker='bytetrack.yaml', save_txt=True, save_conf=True, save_crop=True)