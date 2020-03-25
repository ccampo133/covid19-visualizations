import pystache
from covid19visuals import constants, templates
import importlib.resources as pkg_resources


def build_index_html(total_cases, total_cases_us, total_deaths, total_deaths_us):
    html = pkg_resources.read_text(templates, 'index.html')
    last_updated = f'{constants.NOW.replace(microsecond=0).strftime("%A, %d %B %Y, %H:%M %Z")}'
    template_data = {
        'total_cases': f'{total_cases:,}',
        'total_cases_us': f'{total_cases_us:,}',
        'total_deaths': f'{total_deaths:,}',
        'total_deaths_us': f'{total_deaths_us:,}',
        'last_updated': last_updated
    }
    rendered = pystache.render(html, template_data)
    with open('index.html', 'w') as f:
        f.write(rendered)
    print('Saved file: index.html')
