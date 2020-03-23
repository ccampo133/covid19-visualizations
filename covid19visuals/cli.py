import pandas as pd
from datetime import datetime
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
TIME_SERIES_BASE_URL = f'{BASE_URL}/csse_covid_19_time_series'
CONFIRMED_GLOBAL_TIME_SERIES = f'{TIME_SERIES_BASE_URL}/time_series_covid19_confirmed_global.csv'
CONFIRMED_REGIONAL_TIME_SERIES = f'{TIME_SERIES_BASE_URL}/time_series_19-covid-Confirmed.csv'
GLOBAL_DATE_FORMAT = '%m/%d/%Y'
REGIONAL_DATE_FORMAT = '%m/%d/%y'
TODAY = datetime.now().date()


def main():
    global_confirmed = pd.read_csv(CONFIRMED_GLOBAL_TIME_SERIES)
    regional_confirmed = pd.read_csv(CONFIRMED_REGIONAL_TIME_SERIES)
    fig, ax = plt.subplots()
    plot_country_regional(ax, regional_confirmed, 'US')
    plot_country_regional(ax, regional_confirmed, 'Italy')
    plot_country_regional(ax, regional_confirmed, 'United Kingdom')
    plot_country_regional(ax, regional_confirmed, 'Spain')
    plot_country_regional(ax, regional_confirmed, 'France')
    plot_country_regional(ax, regional_confirmed, 'Germany')
    ax.set_xlabel(f"Days from {datetime.today().date().strftime('%d %B %Y')}")
    ax.set_ylabel('Confirmed COVID-19 Cases')
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.grid(linestyle='-.', linewidth=0.25)
    ax.legend(prop={'size': 6})
    fig.tight_layout()

    plt.show()


def plot_country(ax, data: DataFrame, country: str):
    country_data = data.query(f'`Country/Region` == "{country}" & `Province/State` != `Province/State`')
    days, cases = [], []
    for col in country_data.columns.values:
        try:
            date = datetime.strptime(col, GLOBAL_DATE_FORMAT).date()
        except ValueError:
            date = None

        if date is not None:
            delta = (date - TODAY).days
            if delta >= -30:
                days.append(delta)
                cases.append(country_data[col].values[0])

    diff = cases[-1] - cases[-2]
    ax.semilogy(days, cases, 's-', ms=3, label=f'{country} (+{diff})')


def plot_country_regional(ax, data: DataFrame, country: str):
    regional_data = data.query(f'`Country/Region` == "{country}"')
    days, cases = [], []

    for col in regional_data.columns.values:
        try:
            date = datetime.strptime(col, REGIONAL_DATE_FORMAT).date()
        except ValueError:
            date = None

        if date is not None:
            delta = (date - TODAY).days
            if delta >= -70:
                days.append(delta)
                cases.append(regional_data[col].sum())

    diff = cases[-1] - cases[-2]
    ax.semilogy(days, cases, 's-', ms=3, label=f'{country} (+{diff})')


if __name__ == '__main__':
    main()
