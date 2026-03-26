class TableTracker:
    """
    Класс для определения состояния:
    approach: человек стабильно появился
    empty: человек стабильно ушёл
    """
    def __init__(self, threshold=5):
        self.state = "EMPTY"
        self.buffer = 0   # счетчик "уверенности", что человек есть
        self.threshold = threshold   # количество кадров подряд для подтверждения
        self.events = []

    def update(self, has_person: bool, timestamp: float) -> str:
        """Преобразует сигнал в событие"""
        if has_person:
            self.buffer += 1
        else:
            self.buffer -= 1

        self.buffer = max(0, min(self.buffer, self.threshold))
        stable_has_person = self.buffer >= self.threshold

        if self.state == "EMPTY" and stable_has_person:  # человек стабильно появился
            self.state = "OCCUPIED"
            self.events.append(("approach", timestamp))

        elif self.state == "OCCUPIED" and not stable_has_person:  # человек стабильно ушёл
            self.state = "EMPTY"
            self.events.append(("empty", timestamp))

        return self.state
