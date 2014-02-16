from flask import Flask

from .util import import_string


BLUEPRINTS = [
    ('.home:bp', {}),
]


class Application(Flask):
    def initialize(self):
        for location, options in BLUEPRINTS:
            bp = import_string(location, 'githubarium')
            self.register_blueprint(bp, **options)

app = Application(__name__)
app.config.from_object('githubarium.default_config')
