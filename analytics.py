import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

MIN_OCCUPANCY = 4.0  # человек должен сидеть минимум 4 секунды
MIN_DELAY = 2.5  # минимальная задержка между уходом и следующим подходом


def compute_average_delay(events: list, save_path: str | None = None) -> tuple[float | int, DataFrame]:
    """
    Считает среднее время ожидания стола:
    учитываются только "валидные" occupancy (достаточно длинные)
    """
    if not events:
        return 0.0, pd.DataFrame(columns=["event", "time"])
    df = pd.DataFrame(events, columns=["event", "time"])

    delays = []
    last_empty_time = None  # последнее валидное освобождение стола
    current_approach_time = None  # текущий визит

    for _, row in df.iterrows():
        event = row["event"]
        time = row["time"]

        if event == "approach":
            current_approach_time = time

            if last_empty_time is not None:
                delay = time - last_empty_time
                if delay >= MIN_DELAY:
                    delays.append(delay)

        elif event == "empty":
            if current_approach_time is not None:  # проверяем, что это был "настоящий визит"
                occupancy_duration = time - current_approach_time

                if occupancy_duration >= MIN_OCCUPANCY:
                    last_empty_time = time
            current_approach_time = None

    if save_path:
        df.to_csv(save_path, index=False)
    avg_delay = round(sum(delays) / len(delays), 2) if delays else 0.0
    print(f"Valid delays found: {len(delays)} → {delays}")
    print(f"Average delay: {avg_delay} seconds")
    return avg_delay, df
