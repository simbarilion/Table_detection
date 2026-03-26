from typing import Any


def iou(box: tuple, roi: Any) -> float:
    """Вычисляет, насколько человек "внутри" стола (площадь пересечения)"""
    x1, y1, x2, y2 = box  # человек
    rx, ry, rw, rh = roi # стол

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

    return inter_area / union if union > 0 else 0.0

def person_score(box: Any, roi: Any, min_iou=0.05) -> float:
    """
    Смешанный скоринг:
    - пересечение
    - расстояние до центра стола
    """
    x1, y1, x2, y2 = box  # человек
    rx, ry, rw, rh = roi  # стол

    cx = (x1 + x2) / 2  # центр человека
    cy = (y1 + y2) / 2

    roi_cx = rx + rw / 2  # центр стола
    roi_cy = ry + rh / 2

    dist = ((cx - roi_cx)**2 + (cy - roi_cy)**2) ** 0.5  # расстояние
    max_dist = (rw + rh) / 3

    dist_score = max(0, 1 - (dist / max_dist))
    iou_val = iou(box, roi)

    if iou_val < min_iou:
        iou_val *= 0.5

    return 0.7 * iou_val + 0.4 * dist_score
