import argparse

import pandas as pd

from covid19visuals import constants, plotting, templating, analysis

select_countries = [
    'US',
    'Italy',
    'United Kingdom',
    'Spain',
    'Germany',
    'France',
    'Iran',
    'Belgium',
    'Netherlands'
]

select_states = [
    'New York',
    'New Jersey',
    'California',
    'Michigan',
    'Florida',
    'Massachusetts',
    'Washington',
    'Louisiana',
    'Illinois'
]


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
    plotting.rates.plot_death_rate_select_countries(deaths, cases, select_countries + ['China'],
                                                    latest=args.latest_only)

    plotting.timeseries.plot_cases_select_states(us_data, select_states, latest=args.latest_only)
    plotting.timeseries.plot_deaths_select_states(us_data, select_states, latest=args.latest_only)
    plotting.rates.plot_death_rate_select_states(us_data, select_states, latest=args.latest_only)

    if not args.no_html:
        total_cases = analysis.get_latest_total(cases)
        total_deaths = analysis.get_latest_total(deaths)
        total_cases_us = analysis.get_latest_total(cases, 'US')
        total_deaths_us = analysis.get_latest_total(deaths, 'US')
        templating.build_index_html(total_cases, total_cases_us, total_deaths, total_deaths_us)


if __name__ == '__main__':
    main()
