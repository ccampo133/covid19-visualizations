from typing import List

import pandas as pd
from datetime import datetime
from covid19visuals import constants, utils
import numpy as np

from matplotlib import pyplot as plt, ticker

MIN_DEATHS = 10
CASES_Y_LABEL = 'Confirmed COVID-19 Cases'
CASES_X_LABEL = f"Days from {constants.TODAY.strftime('%d %B %Y')}"
DEATHS_Y_LABEL = 'Confirmed COVID-19 Deaths'
DEATHS_X_LABEL = f"Days since {MIN_DEATHS} deaths"


def plot_death_rate_select_countries(deaths: pd.DataFrame, cases: pd.DataFrame, countries: List[str]):
    fig, ax = plt.subplots(dpi=135)

    death_rates = {}
    for country in countries:
        death_rate = _get_death_rate(
            deaths.query(f'`Country/Region` == "{country}"'),
            cases.query(f'`Country/Region` == "{country}"')
        )
        death_rates[country] = death_rate

    # Sort by death rate
    death_rates = {k: v for k, v in sorted(death_rates.items(), key=lambda item: item[1])}
    y_pos = np.arange(len(death_rates))
    ax.barh(y_pos, death_rates.values(), align='center')

    # Add percentages at ends of bars
    for i, v in enumerate(death_rates.values()):
        ax.text(v + 0.01, i - 0.05, f'{str(round(v, 1))}%')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(death_rates.keys())
    ax.set_xlim([0, 11])
    ax.tick_params(axis='x', labelsize=8)
    ax.grid(axis='x', alpha=0.5)
    ax.xaxis.tick_top()
    ax.set_axisbelow(True)
    ax.set_title(f"Death Rate (as of {constants.TODAY.strftime('%d %B %Y')})")
    _add_watermark(ax, ypos=-0.05)
    fig.tight_layout()
    _save_figs(fig, 'death_rate_select_countries')


def plot_deaths_select_countries(deaths: pd.DataFrame, countries: List[str]):
    fig, ax = plt.subplots(dpi=135)

    max_x, max_y = 0, 1e4
    for country in countries:
        x, y = _get_days_deaths(deaths.query(f'`Country/Region` == "{country}"'), MIN_DEATHS)
        cur_max_x = max(x)
        cur_max_y = max(y)
        if cur_max_x > max_x:
            max_x = cur_max_x
        if cur_max_y > max_y:
            max_y = 1e5
        _plot_semilogy(ax, x, y, country)

    title = 'Deaths (Select Countries)'

    _config_axes(ax, xlim=[0, max_x + 1], ylim=[10, max_y], xlabel=DEATHS_X_LABEL, ylabel=DEATHS_Y_LABEL, title=title)
    fig.tight_layout()
    _save_figs(fig, 'deaths_select_countries')


def plot_cases_select_countries(cases: pd.DataFrame, countries: List[str]):
    fig, ax = plt.subplots(dpi=135)

    max_y = 1e5
    for country in countries:
        x, y = _get_days_cases(cases.query(f'`Country/Region` == "{country}"'))
        cur_max_y = max(y)
        if cur_max_y > max_y:
            max_y = 1e6
        _plot_semilogy(ax, x, y, country)

    title = 'Confirmed Cases (Select Countries)'

    _config_axes(ax, xlim=[-35, 0], ylim=[1, max_y], xlabel=CASES_X_LABEL, ylabel=CASES_Y_LABEL, title=title)
    fig.tight_layout()
    _save_figs(fig, 'confirmed_select_countries')


def plot_cases_select_states(cases: pd.DataFrame, states: List[str]):
    fig, ax = plt.subplots(dpi=135)

    max_y = 1e4
    for state in states:
        x, y = _get_days_cases(cases.query(f'`Country/Region` == "US" & `Province/State` == "{state}"'))
        cur_max_y = max(y)
        if cur_max_y > max_y:
            max_y = 1e5
        _plot_semilogy(ax, x, y, state)

    title = 'Confirmed Cases (Select US States)'

    _config_axes(ax, xlim=[-15, 0], ylim=[1, max_y], xlabel=CASES_X_LABEL, ylabel=CASES_Y_LABEL, title=title)
    fig.tight_layout()
    _save_figs(fig, 'confirmed_select_states')


def _save_figs(fig, fname_prefix: str):
    filenames = [f"{fname_prefix}_latest.png", f"{fname_prefix}_{constants.NOW.strftime('%Y_%m_%d_%H_%M')}.png"]
    for filename in filenames:
        fig.savefig(filename)
        print(f'Saved file: {filename}')


def _config_axes(ax, xlim, ylim, xlabel, ylabel, title):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.grid(linestyle='-.', linewidth=0.25)
    ax.legend(prop={'size': 6}, loc='lower right')
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    ax.set_title(title)
    _add_watermark(ax)


def _get_days_deaths(data: pd.DataFrame, starting_deaths):
    x, y = [], []

    # Parse only the date columns
    t0 = None
    for col in data.columns.values[4:]:
        deaths = data[col].sum()
        if deaths >= starting_deaths:
            date = datetime.strptime(col, constants.REGIONAL_DATE_FORMAT).date()
            if t0 is None:
                t0 = date
            delta = (date - t0).days
            x.append(delta)
            y.append(data[col].sum())

    return x, y


def _get_days_cases(data: pd.DataFrame):
    x, y = [], []

    # Parse only the date columns
    for col in data.columns.values[4:]:
        date = datetime.strptime(col, constants.REGIONAL_DATE_FORMAT).date()
        delta = (date - constants.TODAY).days
        x.append(delta)
        y.append(data[col].sum())

    return x, y


def _get_death_rate(deaths: pd.DataFrame, cases: pd.DataFrame):
    latest_date = deaths.columns.values[-1]
    total_cases = cases[latest_date].sum()
    total_deaths = deaths[latest_date].sum()
    return 100 * (total_deaths / total_cases)


def _plot_semilogy(ax, x, y, region: str):
    pct_change = utils.percent_change(y[-2], y[-1])
    ax.semilogy(x, y, 's-', ms=2.5, linewidth=1, label=f'{region} (+{pct_change}%)')


def _add_watermark(ax, xpos=0.835, ypos=-0.12):
    ax.text(xpos, ypos, '© 2020 C. Campo\ncovid19.ccampo.me', alpha=0.5, fontsize=6, transform=ax.transAxes)
