import pandas as pd

from covid19visuals import constants, plotting, templating, analysis


def main():
    cases = pd.read_csv(constants.CONFIRMED_GLOBAL_TIME_SERIES)
    deaths = pd.read_csv(constants.DEATHS_GLOBAL_TIME_SERIES)

    select_countries = ['US', 'Italy', 'United Kingdom', 'Spain', 'Germany', 'France', 'Iran']
    plotting.plot_cases_select_countries(cases, select_countries)
    plotting.plot_deaths_select_countries(deaths, select_countries)
    plotting.plot_death_rate_select_countries(deaths, cases, select_countries + ['China'])
    # TODO: the regional data is deprecated, which had the state breakdown. Need to wait for US data. -ccampo 2020-03-23
    # select_states = ['Washington', 'New York', 'Florida', 'California', 'New Jersey', 'Illinois']
    # plotting.plot_select_states(confirmed, select_states)

    total_cases = analysis.get_latest_total(cases)
    total_deaths = analysis.get_latest_total(deaths)
    total_cases_us = analysis.get_latest_total(cases, 'US')
    total_deaths_us = analysis.get_latest_total(deaths, 'US')

    templating.build_index_html(total_cases, total_cases_us, total_deaths, total_deaths_us)


if __name__ == '__main__':
    main()
