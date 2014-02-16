import pytest
from githubarium.util import import_string

import json
from os import path
import wave
from logging.handlers import QueueListener


@pytest.mark.parametrize('location, expected', [
    ('json', json),
    ('os.path', path),
    ('wave:open', wave.open),
    ('logging.handlers:QueueListener', QueueListener),
])
def test_import_string_identical(location, expected):
    assert import_string(location) is expected


@pytest.mark.parametrize('location, expected', [
    ('string:ascii_lowercase', 'abcdefghijklmnopqrstuvwxyz'),
    ('pickle:HIGHEST_PROTOCOL', 3),
])
def test_import_string_equals(location, expected):
    assert import_string(location) == expected


def test_import_string_with_absent_module():
    e = pytest.raises(ImportError, import_string, 'flying_spaghetti')
    assert e.value.name == 'flying_spaghetti'
    del e


def test_import_string_with_absent_object():
    e = pytest.raises(AttributeError, import_string, 'json:run_javascript')
    assert repr('run_javascript') in str(e.value)
    del e
