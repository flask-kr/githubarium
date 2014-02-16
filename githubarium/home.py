from flask import Blueprint, render_template
from .user import github, authenticated


bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    if not authenticated():
        return render_template('welcome.html')
    else:
        resp = github.get('user/starred')
        return render_template('index.html', data=resp.data)
