from typing import Any

import torch
from ultralytics import YOLO

class PersonDetector:
    """
    Преобразует изображение в список координат людей.
    Возвращает people = [(x1, y1, x2, y2), ...]
    """
    def __init__(self, model_path="yolov8n.pt", conf=0.3):
        self.device = 0 if torch.cuda.is_available() else "cpu"
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame: Any) -> list:
        results = self.model(
            frame,
            verbose=False,
            imgsz=416,
            conf=self.conf,
            device=self.device,
            max_det=20
        )[0]   # YOLO анализирует кадр

        people = []
        for box in results.boxes:  # список bounding boxes (массивов PyTorch)
            cls = int(box.cls[0])
            confidence = float(box.conf[0])
            if cls != 0 or confidence <= self.conf:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            width = x2 - x1
            height = y2 - y1
            area = width * height
            if height >= 30 and width >= 10 and area >= 500:
                people.append((x1, y1, x2, y2))

        return people
