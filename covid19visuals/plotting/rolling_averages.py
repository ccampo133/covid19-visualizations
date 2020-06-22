from typing import List, Dict, Callable

import numpy as np
import pandas as pd

from covid19visuals import analysis
from covid19visuals.plotting import plotting_utils


def plot_new_cases_seven_day_average_select_countries(
        cases: pd.DataFrame,
        countries: List[Dict],
        latest=False
):
    min_cases = 100
    plot_select_regions(
        data=cases,
        query_func=lambda region: f'`Country/Region` == "{region}"',
        regions_with_pop=countries,
        start=min_cases,
        buffer=10,
        title='Daily Confirmed COVID-19 Cases (Select Countries)\n7-Day Rolling Average (Per 1M Population)',
        xlabel=f'Days since {min_cases} total cases',
        ylabel='Daily cases, 7-day rolling avg. (Per 1M Pop.)',
        fname='daily_confirmed_select_countries',
        latest=latest
    )


def plot_new_cases_seven_day_average_select_states(
        cases: pd.DataFrame,
        countries: List[Dict],
        latest=False,
        fname_suffix=''
):
    min_cases = 100
    plot_select_regions(
        data=cases,
        query_func=lambda region: f'`state` == "{region}"',
        regions_with_pop=countries,
        start=min_cases,
        source_type='nyt',
        col='cases',
        buffer=10,
        title='Daily Confirmed COVID-19 Cases (Select US States)\n7-Day Rolling Average (Per 1M Population)',
        xlabel=f'Days since {min_cases} total cases',
        ylabel='Daily cases, 7-day rolling avg. (Per 1M Pop.)',
        fname='daily_confirmed_select_states' + fname_suffix,
        latest=latest
    )


def plot_new_deaths_seven_day_average_select_countries(
        deaths: pd.DataFrame,
        countries: List[Dict],
        latest=False
):
    min_deaths = 10
    plot_select_regions(
        data=deaths,
        query_func=lambda region: f'`Country/Region` == "{region}"',
        regions_with_pop=countries,
        start=min_deaths,
        buffer=1,
        title='Daily Confirmed COVID-19 Deaths (Select Countries)\n7-Day Rolling Average (Per 1M Population)',
        xlabel=f'Days since {min_deaths} total deaths',
        ylabel='Daily deaths, 7-day rolling avg. (Per 1M Pop.)',
        fname='daily_deaths_select_countries',
        latest=latest
    )


def plot_new_deaths_seven_day_average_select_states(
        deaths: pd.DataFrame,
        countries: List[Dict],
        latest=False,
        fname_suffix=''
):
    min_deaths = 10
    plot_select_regions(
        data=deaths,
        query_func=lambda region: f'`state` == "{region}"',
        regions_with_pop=countries,
        start=min_deaths,
        source_type='nyt',
        col='deaths',
        buffer=1,
        title='Daily Confirmed COVID-19 Deaths (Select US States)\n7-Day Rolling Average (Per 1M Population)',
        xlabel=f'Days since {min_deaths} total deaths',
        ylabel='Daily deaths, 7-day rolling avg. (Per 1M Pop.)',
        fname='daily_deaths_select_states' + fname_suffix,
        latest=latest
    )


def plot_select_regions(
        data: pd.DataFrame,
        query_func: Callable[[str], str],
        regions_with_pop: List[Dict],
        start,
        title: str,
        xlabel,
        ylabel,
        fname: str,
        buffer: int = 1,
        latest=False,
        source_type='jhu',
        col=None
):
    fig, ax = plotting_utils.init_fig()

    max_x, max_y = 0, 0
    for region in regions_with_pop:
        reg, pop = region['region'], region['pop']
        filtered = data.query(query_func(reg))
        x, y = analysis.get_days_new_cases(filtered, start, source_type, col)
        x = x[6:]
        y = analysis.moving_average(y, n=7)
        y = np.array(y) / pop
        cur_max_x, cur_max_y = max(x), max(y)
        if cur_max_x > max_x:
            max_x = cur_max_x
        if cur_max_y > max_y:
            max_y = cur_max_y + buffer
        plotting_utils.plot_linear(ax, x, y, reg)
    plotting_utils.config_axes(
        ax=ax,
        xlim=[6, max_x + 1],
        ylim=[0, max_y],
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        loc='upper left'
    )
    fig.tight_layout()
    plotting_utils.save_figs(fig, fname, latest=latest)
