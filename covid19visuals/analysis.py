from datetime import datetime

import numpy as np
import pandas as pd

from covid19visuals import constants


def get_latest_total(data: pd.DataFrame, country: str = None):
    if country is None:
        filtered = data
    else:
        filtered = data.query(f'`Country/Region` == "{country}"')

    return filtered[filtered.columns.values[-1]].sum()


def get_days_cases(data: pd.DataFrame, start: int):
    days, cases = [], []

    # Parse only the date columns
    t0 = None
    for col in data.columns.values[4:]:
        cur_cases = data[col].sum()
        if cur_cases >= start:
            date = datetime.strptime(col, constants.GLOBAL_DATE_FORMAT).date()
            if t0 is None:
                t0 = date
            delta = (date - t0).days
            days.append(delta)
            cases.append(data[col].sum())

    return days, cases


def get_death_rate(deaths: pd.DataFrame, cases: pd.DataFrame):
    latest_date = deaths.columns.values[-1]
    total_cases = cases[latest_date].sum()
    total_deaths = deaths[latest_date].sum()
    return 100 * (total_deaths / total_cases)


def exponential_growth(t, x0, r):
    return x0 * np.power((1 + r), t)


def doubling_time(r):
    return int(round(0.69 / r))
