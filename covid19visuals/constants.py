from datetime import datetime

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
TIME_SERIES_BASE_URL = f'{BASE_URL}/csse_covid_19_time_series'
CONFIRMED_GLOBAL_TIME_SERIES = f'{TIME_SERIES_BASE_URL}/time_series_covid19_confirmed_global.csv'
CONFIRMED_REGIONAL_TIME_SERIES = f'{TIME_SERIES_BASE_URL}/time_series_19-covid-Confirmed.csv'
GLOBAL_DATE_FORMAT = '%m/%d/%Y'
REGIONAL_DATE_FORMAT = '%m/%d/%y'
NOW = datetime.utcnow()
TODAY = NOW.date()
