from typing import List

import numpy as np
import pandas as pd

from covid19visuals import analysis, constants
from covid19visuals.plotting import plotting_utils


def plot_death_rate_select_countries(deaths: pd.DataFrame, cases: pd.DataFrame, countries: List[str], latest=False):
    fig, ax = plotting_utils.init_fig()

    death_rates = {}
    for country in countries:
        death_rate = analysis.get_death_rate_jhu(
            deaths.query(f'`Country/Region` == "{country}"'),
            cases.query(f'`Country/Region` == "{country}"')
        )
        death_rates[country] = death_rate

    _plot_death_rate(
        death_rates=death_rates,
        fig=fig,
        ax=ax,
        title=f"Global Death Rates (as of {constants.TODAY.strftime('%d %B %Y')})",
        fname='death_rate_select_countries',
        latest=latest
    )


def plot_death_rate_select_states(data: pd.DataFrame, states: List[str], latest=False):
    fig, ax = plotting_utils.init_fig()

    death_rates = {}
    for state in states:
        death_rate = analysis.get_death_rate_nyt(data.query(f'`state` == "{state}"'))
        death_rates[state] = death_rate

    _plot_death_rate(
        death_rates=death_rates,
        fig=fig,
        ax=ax,
        title=f"US Death Rates (as of {constants.TODAY.strftime('%d %B %Y')})",
        fname='death_rate_select_states',
        latest=latest
    )


def _plot_death_rate(death_rates, fig, ax, title, fname, latest=False):
    # Sort by death rate
    death_rates = {k: v for k, v in sorted(death_rates.items(), key=lambda item: item[1])}
    y_pos = np.arange(len(death_rates))
    ax.barh(y_pos, death_rates.values(), align='center')

    # Add percentages at ends of bars
    for i, v in enumerate(death_rates.values()):
        ax.text(v + 0.01, i - 0.05, f'{str(round(v, 1))}%', fontsize=8)

    max_death_rate = max(death_rates.values())
    ax.set_yticks(y_pos)
    ax.set_yticklabels(death_rates.keys())
    ax.set_xlim([0, _get_x_lim_max(max_death_rate)])
    ax.tick_params(axis='x', labelsize=8)
    ax.grid(axis='x', alpha=0.5)
    ax.xaxis.tick_top()
    ax.set_axisbelow(True)
    ax.set_title(title)
    plotting_utils.add_watermark(ax, ypos=-0.05)
    fig.tight_layout()
    plotting_utils.save_figs(fig, fname, latest=latest)


def _get_x_lim_max(x_max):
    decimals = x_max % 1
    if decimals > 0.6:
        return x_max + (1.5 * decimals)
    return x_max + 3.25 * decimals
