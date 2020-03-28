from matplotlib import pyplot as plt

from covid19visuals import constants


def add_watermark(ax, xpos=0.835, ypos=-0.12):
    ax.text(xpos, ypos, '© 2020 C. Campo\ncovid19.ccampo.me', alpha=0.5, fontsize=6, transform=ax.transAxes)


def save_figs(fig, fname_prefix: str, latest=False):
    filenames = [f"{fname_prefix}_latest.png"]
    if not latest:
        filenames.append(f"{fname_prefix}_{constants.NOW.strftime('%Y_%m_%d_%H_%M')}.png")

    for filename in filenames:
        fig.savefig(filename)
        print(f'Saved file: {filename}')


def init_fig():
    return plt.subplots(dpi=constants.DPI)
