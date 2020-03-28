from datetime import datetime, timezone

JHU_BASE_URL = \
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
CONFIRMED_GLOBAL_TIME_SERIES = f'{JHU_BASE_URL}/time_series_covid19_confirmed_global.csv'
DEATHS_GLOBAL_TIME_SERIES = f'{JHU_BASE_URL}/time_series_covid19_deaths_global.csv'
NY_TIMES_BASE_URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master'
US_TIME_SERIES = f'{NY_TIMES_BASE_URL}/us-states.csv'
GLOBAL_DATE_FORMAT = '%m/%d/%y'
STATES_DATE_FORMAT = '%Y-%m-%d'
NOW = datetime.utcnow().replace(tzinfo=timezone.utc)
TODAY = NOW.date()
DPI = 135
