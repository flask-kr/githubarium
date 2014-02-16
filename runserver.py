#!/usr/bin/env python3
import base64
import os.path
from githubarium.web import app


if __name__ == '__main__':
    config_path = os.path.abspath('local.cfg')
    if not os.path.exists(config_path):
        print('Creating default configuration file to {}...'
              .format(config_path))
        with open('local.cfg', 'w', encoding='utf-8') as f:
            secret_key = base64.b64encode(os.urandom(33))
            print('SECRET_KEY = {!r}'.format(secret_key), file=f)
            print("GITHUB_CONSUMER_KEY = ''  # required", file=f)
            print("GITHUB_CONSUMER_SECRET = ''  # required", file=f)
    app.initialize(config_path)
    app.run(debug=True)
