#!/usr/bin/env python3
from githubarium.web import app


if __name__ == '__main__':
    app.initialize()
    app.run(debug=True)
