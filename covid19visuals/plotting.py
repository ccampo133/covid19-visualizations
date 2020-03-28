from typing import List

import pandas as pd
from covid19visuals import constants, utils, analysis
import numpy as np

from matplotlib import pyplot as plt, ticker


def plot_deaths_select_countries(deaths: pd.DataFrame, countries: List[str]):
    min_deaths = 10
    plot_select_countries(
        data=deaths,
        countries=countries,
        start=min_deaths,
        title='Deaths (Select Countries)',
        xlabel=f'Days since {min_deaths} deaths',
        ylabel='Confirmed COVID-19 Deaths',
        fname='deaths_select_countries',
        init_max_x=0,
        init_max_y=1e4,
        step=3
    )


def plot_cases_select_countries(cases: pd.DataFrame, countries: List[str]):
    min_cases = 100
    plot_select_countries(
        data=cases,
        countries=countries,
        start=100,
        title='Confirmed Cases (Select Countries)',
        xlabel=f'Days since {min_cases} cases',
        ylabel='Confirmed COVID-19 Cases',
        fname='confirmed_select_countries',
        init_max_x=0,
        init_max_y=1e5,
        step=3
    )


def plot_select_countries(
        data: pd.DataFrame,
        countries: List[str],
        start,
        title: str,
        xlabel,
        ylabel,
        fname: str,
        init_max_x=0,
        init_max_y=1e5,
        step=10
):
    fig, ax = plt.subplots(dpi=135)

    max_x, max_y = init_max_x, init_max_y
    for country in countries:
        x, y = analysis.get_days_cases(data.query(f'`Country/Region` == "{country}"'), start)
        cur_max_x, cur_max_y = max(x), max(y)
        if cur_max_x > max_x:
            max_x = cur_max_x
        if cur_max_y > max_y:
            max_y *= step
        _plot_semilogy(ax, x, y, country)

    t = np.arange(0, max_x + 2, 1)
    _plot_exponential_growth(ax, start, t, 0.60, linestyle='--')
    _plot_exponential_growth(ax, start, t, 0.35, linestyle='-.')
    _plot_exponential_growth(ax, start, t, 0.25, linestyle=':')
    _config_axes(ax, xlim=[0, max_x + 1], ylim=[start, max_y], xlabel=xlabel, ylabel=ylabel, title=title)
    fig.tight_layout()
    _save_figs(fig, fname)


def plot_death_rate_select_countries(deaths: pd.DataFrame, cases: pd.DataFrame, countries: List[str]):
    fig, ax = plt.subplots(dpi=135)

    death_rates = {}
    for country in countries:
        death_rate = analysis.get_death_rate(
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
        ax.text(v + 0.01, i - 0.05, f'{str(round(v, 1))}%', fontsize=8)

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


def _plot_exponential_growth(ax, x0, t, rate, linestyle='s-'):
    label = f'{int(rate * 100)}% daily increase\n(doubled every {analysis.doubling_time(rate)} days)'
    y = analysis.exponential_growth(t, x0, rate)
    ax.semilogy(t, y, linestyle, ms=2.5, linewidth=1, label=label, color='black', alpha=0.35)


def _plot_semilogy(ax, x, y, region: str):
    pct_change = utils.percent_change(y[-2], y[-1])
    ax.semilogy(x, y, 's-', ms=2.5, linewidth=1, label=f'{region} (+{pct_change}%)')


def _add_watermark(ax, xpos=0.835, ypos=-0.12):
    ax.text(xpos, ypos, '© 2020 C. Campo\ncovid19.ccampo.me', alpha=0.5, fontsize=6, transform=ax.transAxes)
