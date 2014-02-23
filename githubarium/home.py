from collections import defaultdict

from flask import Blueprint, render_template, current_app
from requests.utils import parse_header_links

from .user import github, authenticated


bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    if not authenticated():
        return render_template('welcome.html')
    else:
        data = ()
        if not data:
            buf = defaultdict(list)
            for i in fetch_all_starred_repos():
                buf[i['language']].append(i)
            data = sorted(buf.items(), key=lambda x: len(x[1]) if x[0] else -1,
                          reverse=True)
        return render_template('index.html', data=data)


def fetch_all_starred_repos():
    url = 'user/starred'
    while True:
        current_app.logger.debug('Fetching %s...', url)
        resp = github.get(url)
        yield from resp.data
        link = resp._resp.headers.get('Link', '')
        for i in parse_header_links(link):
            if i['rel'] == 'next':
                url = i['url']
                break
        else:
            return
