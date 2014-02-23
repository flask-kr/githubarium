from flask import (Blueprint, request, session, g,
                   render_template, url_for, redirect, jsonify)
from werkzeug.contrib.cache import SimpleCache
from flask.ext.oauthlib.client import OAuth, OAuthException


bp = Blueprint('user', __name__)

oauth = OAuth()

github = oauth.remote_app(
    'github', app_key='GITHUB',
    request_token_params={'scope': ''},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
)

_cache = SimpleCache()


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


def authenticated():
    """사용자가 GitHub 계정으로 인증한 상태인지 확인한다"""
    try:
        token, _ = session['github_token']
    except KeyError:
        g.user_info = None
        return None
    user_data = _cache.get('user_info:' + token)
    if user_data is None:
        try:
            resp = github.get('user')
        except OAuthException:
            session.pop('github_token', None)
            user_data = None
        else:
            user_data = resp.data
            _cache.set('user_info:' + token, user_data)
    g.user_info = user_data
    return user_data


@bp.route('/login')
def login():
    return github.authorize(callback=url_for('.authorized', _external=True))


@bp.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('home.index'))


@bp.route('/login/authorized')
@github.authorized_handler
def authorized(response):
    if response is None:
        return 'Access denied: reason={reason} error={error}'.format(
            reason=request.args['error_reason'],
            error=request.args['error_description'],
        )
    try:
        github_token = (response['access_token'], '')
    except KeyError:
        if response.get('error') == 'bad_verification_code':
            return redirect(url_for('user.login'))
        else:
            raise
    session['github_token'] = github_token
    return redirect(url_for('home.index'))
