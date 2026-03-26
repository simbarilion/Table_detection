class TableTracker:
    """
    Класс для определения состояния:
    approach: человек стабильно появился
    empty: человек стабильно ушёл
    """
    def __init__(self, threshold=10, min_occupancy_seconds=2.5):
        self.state = "EMPTY"
        self.buffer = 0   # счетчик "уверенности", что человек есть
        self.threshold = threshold   # количество кадров подряд для подтверждения
        self.min_occupancy_seconds = min_occupancy_seconds # минимум сколько должен "посидеть"
        self.events = []
        self.last_approach_time = 0.0

    def update(self, has_person: bool, timestamp: float) -> str:
        """Преобразует сигнал в событие"""
        if has_person:
            self.buffer = min(self.buffer + 1, self.threshold)
        else:
            self.buffer = max(self.buffer - 1, 0)

        stable_has_person = self.buffer >= self.threshold

        if self.state == "EMPTY" and stable_has_person:  # человек стабильно появился
            self.state = "OCCUPIED"
            self.events.append(("approach", timestamp))
            self.last_approach_time = timestamp

        elif self.state == "OCCUPIED" and not stable_has_person:  # человек стабильно ушёл
            occupancy_duration = timestamp - self.last_approach_time
            if occupancy_duration >= self.min_occupancy_seconds:
                self.state = "EMPTY"
                self.events.append(("empty", timestamp))

        return self.state
