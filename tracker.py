class TableTracker:
    """
    Устойчивый трекер состояния стола:
    - защита от кратковременных пропаданий
    - учет минимального времени присутствия
    - задержка перед фиксацией ухода
    approach: человек стабильно появился
    empty: человек стабильно ушёл
    """

    def __init__(self, threshold=12, min_occupancy_seconds=4.0, empty_confirm_seconds=4.0):
        self.state = "EMPTY"
        self.buffer = 0  # счетчик "уверенности", что человек есть
        self.threshold = threshold  # количество кадров подряд для подтверждения
        self.min_occupancy_seconds = min_occupancy_seconds  # фильтр коротких посещений
        self.empty_confirm_seconds = empty_confirm_seconds  # задержка ухода
        self.events = []
        self.last_approach_time = 0.0
        self.last_seen_time = 0.0  # когда последний раз видели человека

    def update(self, has_person: bool, timestamp: float) -> str:
        """
        Преобразует сигнал в событие.
        Обновляет состояние стола с учетом временной устойчивости
        """
        if has_person:
            self.buffer = min(self.buffer + 1, self.threshold)
            self.last_seen_time = timestamp
        else:
            self.buffer = max(self.buffer - 1, 0)

        stable_has_person = self.buffer >= self.threshold

        if self.state == "EMPTY" and stable_has_person:  # человек стабильно появился
            self.state = "OCCUPIED"
            self.last_approach_time = timestamp
            self.events.append(("approach", timestamp))
            return self.state

        if self.state == "OCCUPIED" and not stable_has_person:  # человек стабильно ушёл
            time_since_seen = timestamp - self.last_seen_time

            if time_since_seen >= self.empty_confirm_seconds:
                occupancy_duration = timestamp - self.last_approach_time

                if occupancy_duration >= self.min_occupancy_seconds:  # фильтр коротких попаданий
                    self.state = "EMPTY"
                    self.events.append(("empty", timestamp))

        return self.state
