import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

MIN_OCCUPANCY = 3.0

def compute_average_delay(events: list, save_path: str| None=None) -> tuple[float | int, DataFrame]:
    """
    Считает среднее время ожидания стола:
    учитываются только "валидные" occupancy (достаточно длинные)
    """
    df = pd.DataFrame(events, columns=["event", "time"])

    delays = []
    last_empty = None
    last_approach = None

    for _, row in df.iterrows():
        event = row["event"]
        time = row["time"]

        if event == "empty":
            if last_approach is not None:  # фиксируем момент освобождения стола
                occupancy_duration = time - last_approach

                if occupancy_duration >= MIN_OCCUPANCY:  # проверяем, что сидели достаточно долго
                    if last_empty is not None:
                        delay = last_approach - last_empty
                        delays.append(delay)

            last_empty = time
            last_approach = None


        elif event == "approach":
            last_approach = time  # фиксируем начало "сидения"

    if save_path:
        df.to_csv(save_path, index=False)
    avg_delay = sum(delays) / len(delays) if delays else 0
    return avg_delay, df
