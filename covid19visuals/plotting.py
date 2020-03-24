from typing import List

import pandas as pd
from datetime import datetime
from covid19visuals import constants, utils

from matplotlib import pyplot as plt, ticker


def plot_select_countries(confirmed: pd.DataFrame, countries: List[str]):
    fig, ax = plt.subplots(dpi=135)

    for country in countries:
        _plot_semilogy(ax, confirmed.query(f'`Country/Region` == "{country}"'), country)

    _config_axes(ax, xlim=[-45, 0], ylim=[1, 1e5], title='Confirmed Cases (Select Countries)')
    fig.tight_layout()
    _save_figs(fig, 'confirmed_select_countries')


def plot_select_states(confirmed: pd.DataFrame, states: List[str]):
    fig, ax = plt.subplots(dpi=135)

    for state in states:
        _plot_semilogy(ax, confirmed.query(f'`Country/Region` == "US" & `Province/State` == "{state}"'), state)

    _config_axes(ax, xlim=[-13, 0], ylim=[1, 1e5], title='Confirmed Cases (Select US States)')
    fig.tight_layout()
    _save_figs(fig, 'confirmed_select_states')


def _save_figs(fig, fname_prefix: str):
    filenames = [f"{fname_prefix}_latest.png", f"{fname_prefix}_{constants.NOW.strftime('%Y_%m_%d_%H_%M')}.png"]
    for filename in filenames:
        fig.savefig(filename)
        print(f'Saved file: {filename}')


def _config_axes(ax, xlim, ylim, title):
    ax.set_xlabel(f"Days from {constants.TODAY.strftime('%d %B %Y')}")
    ax.set_ylabel('Confirmed COVID-19 Cases')
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.grid(linestyle='-.', linewidth=0.25)
    ax.legend(prop={'size': 6})
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    ax.set_title(title)
    ax.text(.835, -0.12, '© 2020 C. Campo\ncovid19.ccampo.me', alpha=0.5, fontsize=6, transform=ax.transAxes)


def _plot_semilogy(ax, data: pd.DataFrame, region: str):
    days, cases = [], []

    # Parse only the date columns
    for col in data.columns.values[4:]:
        date = datetime.strptime(col, constants.REGIONAL_DATE_FORMAT).date()
        delta = (date - constants.TODAY).days
        days.append(delta)
        cases.append(data[col].sum())

    pct_change = utils.percent_change(cases[-2], cases[-1])
    ax.semilogy(days, cases, 's-', ms=2.5, label=f'{region} (+{pct_change}%)')
