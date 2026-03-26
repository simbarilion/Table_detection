from typing import Any

from ultralytics import YOLO

class PersonDetector:
    """
    Преобразует изображение в список координат людей.
    Возвращает people = [(x1, y1, x2, y2), ...]
    """
    def __init__(self, model_path="yolov8n.pt", conf=0.4):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame: Any) -> list:
        results = self.model(frame)[0]   # YOLO анализирует кадр

        people = []
        for box in results.boxes:  # список bounding boxes (массивов PyTorch)
            cls = int(box.cls[0])
            confidence = float(box.conf[0])
            if cls == 0 and confidence > self.conf:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                people.append((x1, y1, x2, y2))

        return people
