from typing import List, Callable

import numpy as np
import pandas as pd

from covid19visuals import analysis
from covid19visuals.plotting import plotting_utils


def plot_cases_select_countries(cases: pd.DataFrame, countries: List[str], latest=False):
    min_cases = 100
    plot_select_regions(
        data=cases,
        query_func=lambda region: f'`Country/Region` == "{region}"',
        regions=countries,
        start=100,
        title='Confirmed COVID-19 Cases (Select Countries)',
        xlabel=f'Days since {min_cases} cases',
        ylabel='Cases',
        fname='confirmed_select_countries',
        init_max_x=0,
        init_max_y=2e6,
        step=2,
        latest=latest
    )


def plot_cases_select_states(data: pd.DataFrame, states: List[str], latest=False, fname_suffix=''):
    min_cases = 100
    plot_select_regions(
        data=data,
        query_func=lambda region: f'`state` == "{region}"',
        regions=states,
        start=min_cases,
        source_type='nyt',
        col='cases',
        title='Confirmed COVID-19 Cases (Select US States)',
        xlabel=f'Days since {min_cases} cases',
        ylabel='Cases',
        fname='confirmed_select_states' + fname_suffix,
        init_max_x=0,
        init_max_y=5e5,
        step=2,
        latest=latest
    )


def plot_deaths_select_countries(deaths: pd.DataFrame, countries: List[str], latest=False):
    min_deaths = 10
    plot_select_regions(
        data=deaths,
        query_func=lambda region: f'`Country/Region` == "{region}"',
        regions=countries,
        start=min_deaths,
        title='Confirmed COVID-19 Deaths (Select Countries)',
        xlabel=f'Days since {min_deaths} deaths',
        ylabel='Deaths',
        fname='deaths_select_countries',
        init_max_x=0,
        init_max_y=1e5,
        step=2,
        latest=latest
    )


def plot_deaths_select_states(deaths: pd.DataFrame, states: List[str], latest=False, fname_suffix=''):
    min_deaths = 10
    plot_select_regions(
        data=deaths,
        query_func=lambda region: f'`state` == "{region}"',
        regions=states,
        start=min_deaths,
        source_type='nyt',
        col='deaths',
        title='Confirmed COVID-19 Deaths (Select US States)',
        xlabel=f'Days since {min_deaths} deaths',
        ylabel='Deaths',
        fname='deaths_select_states' + fname_suffix,
        init_max_x=0,
        init_max_y=3e4,
        step=2,
        latest=latest
    )


def plot_select_regions(
        data: pd.DataFrame,
        query_func: Callable[[str], str],
        regions: List[str],
        start,
        title: str,
        xlabel,
        ylabel,
        fname: str,
        init_max_x=0,
        init_max_y=1e5,
        step=10,
        latest=False,
        source_type='jhu',
        col=None
):
    fig, ax = plotting_utils.init_fig()

    max_x, max_y = init_max_x, init_max_y
    for region in regions:
        filtered = data.query(query_func(region))
        x, y = analysis.get_days_cases(filtered, start, source_type, col)
        cur_max_x, cur_max_y = max(x), max(y)
        if cur_max_x > max_x:
            max_x = cur_max_x
        if cur_max_y > max_y:
            max_y *= step
        plotting_utils.plot_semilogy(ax, x, y, region)

    t = np.arange(0, max_x + 2, 1)
    plotting_utils.plot_exponential_growth(ax, start, t, 0.60, ls='--')
    plotting_utils.plot_exponential_growth(ax, start, t, 0.35, ls='-.')
    plotting_utils.plot_exponential_growth(ax, start, t, 0.25, ls=':')
    plotting_utils.config_axes(
        ax=ax,
        xlim=[0, max_x + 1],
        ylim=[start, max_y],
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        ncol=2
    )
    fig.tight_layout()
    plotting_utils.save_figs(fig, fname, latest=latest)
