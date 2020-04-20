import argparse

import pandas as pd

from covid19visuals import constants, plotting, templating, analysis

# Population values in millions. Estimate as of 2020-04-20
# Source: https://www.worldometers.info/world-population/population-by-country/
select_countries_with_populations = [
    {'region': 'US', 'pop': 331002651e-6},
    {'region': 'Italy', 'pop': 60461826e-6},
    {'region': 'United Kingdom', 'pop': 67886011e-6},
    {'region': 'Spain', 'pop': 46754778e-6},
    {'region': 'Germany', 'pop': 83783942e-6},
    {'region': 'France', 'pop': 65273511e-6},
    {'region': 'Iran', 'pop': 83992949e-6},
    {'region': 'Belgium', 'pop': 11589623e-6},
    {'region': 'Netherlands', 'pop': 17134872e-6},
]

# Population values in millions. Estimate as of 2019-07-01
# Source: https://simple.wikipedia.org/wiki/List_of_U.S._states_by_population
select_states_with_populations = [
    {'region': 'New York', 'pop': 19453561e-6},
    {'region': 'New Jersey', 'pop': 8882190e-6},
    {'region': 'California', 'pop': 39512223e-6},
    {'region': 'Michigan', 'pop': 9986857e-6},
    {'region': 'Florida', 'pop': 21477737e-6},
    {'region': 'Massachusetts', 'pop': 6949503e-6},
    {'region': 'Washington', 'pop': 7614893e-6},
    {'region': 'Louisiana', 'pop': 4648794e-6},
    {'region': 'Illinois', 'pop': 12671821e-6},
]

select_countries = [country['region'] for country in select_countries_with_populations]
select_states = [state['region'] for state in select_states_with_populations]


def main():
    parser = argparse.ArgumentParser(description='Generate COVID-19 visualizations')
    parser.add_argument('--latest-only', action='store_true', required=False, help='Save only the latest images.')
    parser.add_argument('--no-html', action='store_true', required=False, help='Do not render index.html.')
    args = parser.parse_args()

    cases = pd.read_csv(constants.CONFIRMED_GLOBAL_TIME_SERIES)
    deaths = pd.read_csv(constants.DEATHS_GLOBAL_TIME_SERIES)
    us_data = pd.read_csv(constants.US_TIME_SERIES)

    plotting.timeseries.plot_cases_select_countries(cases, select_countries, latest=args.latest_only)
    plotting.timeseries.plot_deaths_select_countries(deaths, select_countries, latest=args.latest_only)
    plotting.rates.plot_death_rate_select_countries(deaths, cases, select_countries, latest=args.latest_only)

    plotting.rolling_averages.plot_new_cases_seven_day_average_select_countries(
        cases,
        select_countries_with_populations,
        latest=args.latest_only
    )

    plotting.rolling_averages.plot_new_deaths_seven_day_average_select_countries(
        deaths,
        select_countries_with_populations,
        latest=args.latest_only
    )

    plotting.timeseries.plot_cases_select_states(us_data, select_states, latest=args.latest_only)
    plotting.timeseries.plot_deaths_select_states(us_data, select_states, latest=args.latest_only)
    plotting.rates.plot_death_rate_select_states(us_data, select_states, latest=args.latest_only)
    plotting.rolling_averages.plot_new_cases_seven_day_average_select_states(
        us_data,
        select_states_with_populations,
        latest=args.latest_only
    )

    plotting.rolling_averages.plot_new_deaths_seven_day_average_select_states(
        us_data,
        select_states_with_populations,
        latest=args.latest_only
    )

    if not args.no_html:
        total_cases = analysis.get_latest_total(cases)
        total_deaths = analysis.get_latest_total(deaths)
        total_cases_us = analysis.get_latest_total(cases, 'US')
        total_deaths_us = analysis.get_latest_total(deaths, 'US')
        templating.build_index_html(total_cases, total_cases_us, total_deaths, total_deaths_us)


if __name__ == '__main__':
    main()
