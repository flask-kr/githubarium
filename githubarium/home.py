import json
from flask import Blueprint, render_template


bp = Blueprint('home', __name__)


@bp.route('/')
def home():
    signed_in = False
    if not signed_in:
        return render_template('welcome.html')
    else:
        with open('data.json', encoding='utf-8') as f:
            sample_data = json.load(f)
        return render_template('index.html', data=sample_data)
