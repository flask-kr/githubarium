import collections

from flask import Flask

from .util import import_string
from .user import oauth, authenticated


BLUEPRINTS = [
    ('.home:bp', {}),
    ('.user:bp', {}),
]


class Application(Flask):
    def initialize(self, config=None):
        if config is not None:
            self.update_config(config)
        oauth.init_app(self)
        for location, options in BLUEPRINTS:
            bp = import_string(location, 'githubarium')
            self.register_blueprint(bp, **options)

    def update_config(self, config):
        if isinstance(config, str):
            self.config.from_pyfile(config)
        elif isinstance(config, collections.Mapping):
            self.config.update(config)
        else:
            self.config.from_object(config)

app = Application(__name__)
app.config.from_object('githubarium.default_config')
app.jinja_env.globals['authenticated'] = authenticated
