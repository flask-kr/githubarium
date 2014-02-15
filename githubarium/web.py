from flask import Flask, render_template
import json

with open('data.json', encoding='utf-8') as f:
    SAMPLE_DATA = json.load(f)


class Application(Flask):
    def initialize(self):
        pass

app = Application(__name__)
app.config.from_object('githubarium.default_config')


@app.route('/')
def home():
    return render_template('index.html', data=SAMPLE_DATA)
