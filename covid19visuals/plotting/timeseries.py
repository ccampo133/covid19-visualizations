from typing import List, Callable

import numpy as np
import pandas as pd
from matplotlib import ticker

from covid19visuals import utils, analysis
from covid19visuals.plotting import plotting_utils


def plot_cases_select_states(data: pd.DataFrame, states: List[str], latest=False):
    min_cases = 100
    plot_select_regions(
        data=data,
        query_func=lambda region: f'`state` == "{region}"',
        regions=states,
        start=min_cases,
        type='nyt',
        col='cases',
        title='Confirmed Cases (Select US States)',
        xlabel=f'Days since {min_cases} cases',
        ylabel='Confirmed COVID-19 Cases',
        fname='confirmed_select_states',
        init_max_x=0,
        init_max_y=1e5,
        step=6,
        latest=latest
    )


def plot_deaths_select_states(deaths: pd.DataFrame, states: List[str], latest=False):
    min_deaths = 10
    plot_select_regions(
        data=deaths,
        query_func=lambda region: f'`state` == "{region}"',
        regions=states,
        start=min_deaths,
        type='nyt',
        col='deaths',
        title='Deaths (Select US States)',
        xlabel=f'Days since {min_deaths} deaths',
        ylabel='Confirmed COVID-19 Deaths',
        fname='deaths_select_states',
        init_max_x=0,
        init_max_y=1e3,
        step=10,
        latest=latest
    )


def plot_deaths_select_countries(deaths: pd.DataFrame, countries: List[str], latest=False):
    min_deaths = 10
    plot_select_regions(
        data=deaths,
        query_func=lambda region: f'`Country/Region` == "{region}"',
        regions=countries,
        start=min_deaths,
        title='Deaths (Select Countries)',
        xlabel=f'Days since {min_deaths} deaths',
        ylabel='Confirmed COVID-19 Deaths',
        fname='deaths_select_countries',
        init_max_x=0,
        init_max_y=1e4,
        step=6,
        latest=latest
    )


def plot_cases_select_countries(cases: pd.DataFrame, countries: List[str], latest=False):
    min_cases = 100
    plot_select_regions(
        data=cases,
        query_func=lambda region: f'`Country/Region` == "{region}"',
        regions=countries,
        start=100,
        title='Confirmed Cases (Select Countries)',
        xlabel=f'Days since {min_cases} cases',
        ylabel='Confirmed COVID-19 Cases',
        fname='confirmed_select_countries',
        init_max_x=0,
        init_max_y=1e5,
        step=6,
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
        type='jhu',
        col=None
):
    fig, ax = plotting_utils.init_fig()

    max_x, max_y = init_max_x, init_max_y
    for region in regions:
        filtered = data.query(query_func(region))
        x, y = analysis.get_days_cases(filtered, start, type, col)
        cur_max_x, cur_max_y = max(x), max(y)
        if cur_max_x > max_x:
            max_x = cur_max_x
        if cur_max_y > max_y:
            max_y *= step
        _plot_semilogy(ax, x, y, region)

    t = np.arange(0, max_x + 2, 1)
    _plot_exponential_growth(ax, start, t, 0.60, ls='--')
    _plot_exponential_growth(ax, start, t, 0.35, ls='-.')
    _plot_exponential_growth(ax, start, t, 0.25, ls=':')
    _config_axes(ax, xlim=[0, max_x + 1], ylim=[start, max_y], xlabel=xlabel, ylabel=ylabel, title=title)
    fig.tight_layout()
    plotting_utils.save_figs(fig, fname, latest=latest)


def _config_axes(ax, xlim, ylim, xlabel, ylabel, title):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.grid(linestyle='-.', linewidth=0.25)
    ax.legend(prop={'size': 5}, loc='lower right', ncol=2)
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    start, end = xlim
    ax.xaxis.set_ticks(np.arange(start, end + 1, 5))
    ax.set_title(title)
    plotting_utils.add_watermark(ax)


def _plot_exponential_growth(ax, x0, t, rate, ls='s-'):
    label = f'{int(rate * 100)}% daily increase\n(doubled every {analysis.doubling_time(rate)} days)'
    y = analysis.exponential_growth(t, x0, rate)
    ax.semilogy(t, y, linestyle=ls, ms=2.5, linewidth=1, label=label, color='black', alpha=0.35)


def _plot_semilogy(ax, x, y, region: str):
    pct_change = utils.percent_change(y[-2], y[-1])
    ax.semilogy(x, y, 's-', ms=2.5, linewidth=1, label=f'{region} (+{pct_change}%)')
