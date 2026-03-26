from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

CSV_PATH = OUTPUT_DIR / f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
VIDEO_2_PATH = BASE_DIR / "data" / "video_2.mp4"
OUTPUT_PATH = BASE_DIR / "output" / "output_video_2.mp4"
