import pandas as pd

from covid19visuals import constants, plotting, templating


def main():
    templating.build_index_html()
    cases = pd.read_csv(constants.CONFIRMED_GLOBAL_TIME_SERIES)
    deaths = pd.read_csv(constants.DEATHS_GLOBAL_TIME_SERIES)
    select_countries = ['US', 'Italy', 'United Kingdom', 'Spain', 'Germany', 'France', 'Iran']
    plotting.plot_cases_select_countries(cases, select_countries)
    plotting.plot_deaths_select_countries(deaths, select_countries)
    plotting.plot_death_rate_select_countries(deaths, cases, select_countries + ['China'])

    # TODO: the regional data is deprecated, which had the state breakdown. Need to wait for US data. -ccampo 2020-03-23
    # select_states = ['Washington', 'New York', 'Florida', 'California', 'New Jersey', 'Illinois']
    # plotting.plot_select_states(confirmed, select_states)


if __name__ == '__main__':
    main()
