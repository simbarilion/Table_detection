import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame


def compute_average_delay(events: list, save_path: str| None=None) -> tuple[float | int, DataFrame]:
    """Считает, сколько времени стол был пуст до прихода следующего человека"""
    df = pd.DataFrame(events, columns=["event", "time"])

    delays = []
    last_empty = None

    for _, row in df.iterrows():
        if row["event"] == "empty":
            last_empty = row["time"]

        elif row["event"] == "approach" and last_empty is not None:
            delays.append(row["time"] - last_empty)
            last_empty = None

    if save_path:
        df.to_csv(save_path, index=False)
    avg_delay = sum(delays) / len(delays) if delays else 0
    return avg_delay, df
