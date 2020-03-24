import pystache
from covid19visuals import constants, templates
import importlib.resources as pkg_resources


def build_index_html():
    html = pkg_resources.read_text(templates, 'index.html')
    last_updated = f'{constants.NOW.replace(microsecond=0).strftime("%A, %d %B %Y, %H:%M %Z")}'
    rendered = pystache.render(html, {'last_updated': last_updated})
    with open('index.html', 'w') as f:
        f.write(rendered)
    print('Saved file: index.html')
