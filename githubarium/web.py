import collections

from flask import Flask
from flask.helpers import locked_cached_property

from .util import import_string


BLUEPRINTS = [
    ('.home:bp', {}),
    ('.user:bp', {}),
]


class Application(Flask):
    @locked_cached_property
    def package_name(self):
        return self.import_name.rsplit('.', 1)[0]

    def lazy_import(self, import_name, **kwargs):
        return import_string(import_name, self.package_name, **kwargs)

    def initialize(self, config=None):
        if config is not None:
            self.update_config(config)
        self.lazy_import('.user:oauth').init_app(self)
        for location, options in BLUEPRINTS:
            bp = self.lazy_import(location)
            self.register_blueprint(bp, **options)

    def update_config(self, config):
        if isinstance(config, str):
            self.config.from_pyfile(config)
        elif isinstance(config, collections.Mapping):
            self.config.update(config)
        else:
            self.config.from_object(config)

    def create_jinja_environment(self):
        rv = super().create_jinja_environment()
        rv.globals.update(
            authenticated=self.lazy_import('.user:authenticated')
        )
        return rv


app = Application(__name__)
app.config.from_object('githubarium.default_config')
