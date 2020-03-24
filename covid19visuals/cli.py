import pandas as pd

from covid19visuals import constants, plotting, templating


def main():
    templating.build_index_html()
    confirmed = pd.read_csv(constants.CONFIRMED_GLOBAL_TIME_SERIES)
    select_countries = ['US', 'Italy', 'United Kingdom', 'Spain', 'Germany', 'France', 'Iran', 'China']
    plotting.plot_select_countries(confirmed, select_countries)
    # TODO: the regional data is deprecated, which had the state breakdown. Switch to daily reports? -ccampo 2020-03-23
    # select_states = ['Washington', 'New York', 'Florida', 'California', 'New Jersey', 'Illinois']
    # plotting.plot_select_states(confirmed, select_states)


if __name__ == '__main__':
    main()
