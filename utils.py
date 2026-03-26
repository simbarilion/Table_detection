from typing import Any


def iou(box: Any, roi: Any) -> float:
    """Вычисляет, насколько человек "внутри" стола (площадь пересечения)"""
    x1, y1, x2, y2 = box  # человек
    rx, ry, rw, rh = roi  # стол

    rx2 = rx + rw
    ry2 = ry + rh

    inter_x1 = max(x1, rx)
    inter_y1 = max(y1, ry)
    inter_x2 = min(x2, rx2)
    inter_y2 = min(y2, ry2)

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    box_area = (x2 - x1) * (y2 - y1)
    roi_area = rw * rh

    union = box_area + roi_area - inter_area

    return inter_area / union if union > 0 else 0
