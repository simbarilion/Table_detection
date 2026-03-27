.PHONY: lint format run

lint:
	isort . --check-only --diff
	black . --check
	flake8 .

format:
	isort .
	black .

run:
	python main.py --video data/video_2.mp4 --conf 0.3
