import pandas as pd

from covid19visuals import constants, plotting, templating


def main():
    templating.build_index_html()
    confirmed = pd.read_csv(constants.CONFIRMED_REGIONAL_TIME_SERIES)
    plotting.plot_all(confirmed)


if __name__ == '__main__':
    main()
