from pathlib import Path

import cv2
import argparse

from config import CSV_PATH, VIDEO_2_PATH, OUTPUT_PATH
from detector import PersonDetector
from logger import setup_logger
from tracker import TableTracker
from analytics import compute_average_delay
from utils import person_score

logger = setup_logger(__name__, log_to_console=True)

def main(video_path, conf):
    logger.info(f"Start processing video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error("Video not opened!")
    fps = cap.get(cv2.CAP_PROP_FPS)  # частота кадров в секунду видео
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    logger.info(f"FPS: {fps}, total frames: {total_frames}")

    detector = PersonDetector(conf=conf)
    tracker = TableTracker(threshold=10, min_occupancy_seconds=2.5)

    ret, frame = cap.read()
    if not ret:
        logger.error("Failed to read first frame")
        return
    cv2.imshow("Select Table", frame)
    roi = cv2.selectROI("Select Table", frame, fromCenter=False, showCrosshair=False)
    x, y, w, h = roi
    if w == 0 or h == 0:
        logger.error("ROI not selected properly!")
        return
    cv2.destroyWindow("Select Table")
    logger.info(f"ROI selected: {roi}")

    people = detector.detect(frame)
    initial_has_person = any(person_score(p, roi) > 0.2 for p in people)
    tracker.state = "OCCUPIED" if initial_has_person else "EMPTY"
    logger.info(f"Initial state: {tracker.state}")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        OUTPUT_PATH,
        fourcc,
        fps,
        (frame.shape[1], frame.shape[0])
    )
    frame_id = 0
    skip_frames = 3
    last_people = []
    last_has_person = False
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        timestamp = frame_id / fps
        if frame_id % skip_frames == 0:
            roi_frame = frame[y:y + h, x:x + w]
            if roi_frame.size == 0:
                continue
            people_roi = detector.detect(roi_frame)
            people = [(x1 + x, y1 + y, x2 + x, y2 + y)
                      for (x1, y1, x2, y2) in people_roi]
            last_people = people
            has_person = any(person_score(p, roi) > 0.15 for p in people) # 0.15 - эмпирический порог пересечения
            last_has_person = has_person
        else:
            people = last_people
            has_person = last_has_person

        if frame_id % 1000 == 0:
            print(
                f"Frame {frame_id:5d} | detected {len(people):2d} people | has_person={has_person} | buffer={tracker.buffer} | state={tracker.state}")

        for (x1, y1, x2, y2) in people:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        logger.debug(f"Detected {len(people)} people | has_person in ROI: {has_person}")

        state = tracker.update(has_person, timestamp)
        logger.debug(f"State: {state}, buffer: {tracker.buffer}")

        color = (0, 255, 0) if state == "EMPTY" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
        cv2.putText(frame, state, (x, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    avg_delay, df = compute_average_delay(tracker.events, save_path=CSV_PATH)

    print("Average delay:", avg_delay)
    logger.info(f"Finished. Avg delay: {avg_delay}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, default=str(VIDEO_2_PATH))
    parser.add_argument("--conf", type=float, default=0.3)
    args = parser.parse_args()
    video_path = Path(args.video)

    main(video_path, args.conf)
