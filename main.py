import cv2
import argparse

from detector import PersonDetector
from tracker import TableTracker
from analytics import compute_average_delay
from utils import iou


def main(video_path, conf):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    detector = PersonDetector(conf=conf)  # детектор с параметром confidence
    tracker = TableTracker(threshold=5)    # трекер с фильтром

    ret, frame = cap.read()   # читаем первый кадр
    roi = cv2.selectROI("Select Table", frame, False)
    x, y, w, h = roi

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")   # видео writer
    out = cv2.VideoWriter(                     # создаём файл
        "output/output.mp4",
        fourcc,
        fps,
        (frame.shape[1], frame.shape[0])
    )

    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        timestamp = frame_id / fps

        people = detector.detect(frame)   # детекция людей
        has_person = any(iou(p, roi) > 0.2 for p in people)   # есть ли человек у стола, 0.2 - эмпирический порог
        state = tracker.update(has_person, timestamp)  # передаем уже готовый boolean - "есть человек или нет"

        color = (0, 255, 0) if state == "EMPTY" else (0, 0, 255) # визуализация

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, state, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        out.write(frame)  # записываем каждый кадр

        frame_id += 1

    cap.release()
    out.release()   # закрываем файл
    cv2.destroyAllWindows()

    avg_delay, df = compute_average_delay(tracker.events, save_path="events.csv")  # аналитика

    print("Average delay:", avg_delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--conf", type=float, default=0.4)  # CLI параметр теперь можно запускать: python main.py --video video.mp4 --conf 0.3
    args = parser.parse_args()

    main(args.video, args.conf)
