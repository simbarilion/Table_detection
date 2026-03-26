import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

MIN_DURATION = 1.0

def compute_average_delay(events: list, save_path: str| None=None) -> tuple[float | int, DataFrame]:
    """Считает, сколько времени стол был пуст до прихода следующего человека"""
    df = pd.DataFrame(events, columns=["event", "time"])

    delays = []
    last_empty = None

    for _, row in df.iterrows():
        if row["event"] == "empty":
            last_empty = row["time"]

        elif row["event"] == "approach" and last_empty is not None:
            delay = row["time"] - last_empty
            if delay > MIN_DURATION:
                delays.append(delay)
            last_empty = None

    if save_path:
        df.to_csv(save_path, index=False)
    avg_delay = sum(delays) / len(delays) if delays else 0
    return avg_delay, df
