from covid19visuals import constants
import pystache


def build_index_html() -> str:
    with open('templates/index.html', 'r') as tpl:
        html = tpl.read()
    return pystache.render(html, {'last_updated': f'{constants.NOW.replace(microsecond=0).isoformat()}Z'})
