import numpy as np
from matplotlib import pyplot as plt, ticker

from covid19visuals import constants, utils, analysis


def add_watermark(ax, xpos=0.835, ypos=-0.12):
    ax.text(xpos, ypos, '© 2022 C. Campo\ncovid19.ccampo.me', alpha=0.5, fontsize=6, transform=ax.transAxes)


def save_figs(fig, fname_prefix: str, latest=False):
    filenames = [f"{fname_prefix}_latest.png"]
    if not latest:
        filenames.append(f"{fname_prefix}_{constants.NOW.strftime('%Y_%m_%d_%H_%M')}.png")

    for filename in filenames:
        fig.savefig(filename)
        print(f'Saved file: {filename}')


def init_fig():
    return plt.subplots(dpi=constants.DPI)


def config_axes(ax, xlim, ylim, xlabel, ylabel, title, loc='lower right', ncol=1):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.grid(linestyle='-.', linewidth=0.25)
    ax.legend(prop={'size': 5}, loc=loc, ncol=ncol)
    ax.set_ylim(ylim)
    ax.set_xlim(xlim)
    start, end = xlim
    ax.xaxis.set_ticks(np.arange(start, end + 10, 20))
    ax.tick_params(axis='x', labelsize=6)
    ax.set_title(title)
    add_watermark(ax)


def plot_linear(ax, x, y, region: str):
    pct_change = utils.percent_change(y[-2], y[-1])
    sign = '+' if pct_change > 0 else ''
    ax.plot(x, y, '-', ms=1.5, linewidth=1, label=f'{region} ({sign}{pct_change}%)')


def plot_exponential_growth(ax, x0, t, rate, ls='s-'):
    label = f'{int(rate * 100)}% daily increase\n(doubled every {analysis.doubling_time(rate)} days)'
    y = analysis.exponential_growth(t, x0, rate)
    ax.semilogy(t, y, linestyle=ls, ms=1.5, linewidth=1, label=label, color='black', alpha=0.35)


def plot_semilogy(ax, x, y, region: str):
    pct_change = utils.percent_change(y[-2], y[-1])
    ax.semilogy(x, y, '-', ms=1.5, linewidth=1, label=f'{region} (+{pct_change}%)')
