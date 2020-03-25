from datetime import datetime, timezone

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
TIME_SERIES_BASE_URL = f'{BASE_URL}/csse_covid_19_time_series'
CONFIRMED_GLOBAL_TIME_SERIES = f'{TIME_SERIES_BASE_URL}/time_series_covid19_confirmed_global.csv'
DEATHS_GLOBAL_TIME_SERIES = f'{TIME_SERIES_BASE_URL}/time_series_covid19_deaths_global.csv'
CONFIRMED_REGIONAL_TIME_SERIES = f'{TIME_SERIES_BASE_URL}/time_series_19-covid-Confirmed.csv'
GLOBAL_DATE_FORMAT = '%m/%d/%Y'
REGIONAL_DATE_FORMAT = '%m/%d/%y'
NOW = datetime.utcnow().replace(tzinfo=timezone.utc)
TODAY = NOW.date()
