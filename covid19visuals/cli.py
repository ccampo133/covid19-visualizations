import pandas as pd

from covid19visuals import constants, plotting


def main():
    confirmed = pd.read_csv(constants.CONFIRMED_REGIONAL_TIME_SERIES)
    plotting.plot_all(confirmed)


if __name__ == '__main__':
    main()
