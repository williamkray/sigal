# -*- coding:utf-8 -*-

import os
import pytest

from sigal.settings import read_settings, get_thumb, get_orig

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='module')
def settings():
    """Read the sample config file."""
    return read_settings(os.path.join(CURRENT_DIR, 'sample', 'sigal.conf.py'))


def test_read_settings(settings):
    """Test that the settings are correctly read."""
    assert settings['img_size'] == (640, 480)
    assert settings['thumb_size'] == (200, 150)
    assert settings['thumb_suffix'] == '.tn'
    assert settings['source'] == os.path.join(CURRENT_DIR, 'sample',
                                              'pictures')


def test_get_thumb(settings):
    """Test the get_thumb function."""
    tests = [('example.jpg', 'thumbnails/example.tn.jpg'),
             ('test/example.jpg', 'test/thumbnails/example.tn.jpg'),
             ('test/t/example.jpg', 'test/t/thumbnails/example.tn.jpg')]
    for src, ref in tests:
        assert get_thumb(settings, src) == ref


def test_get_orig(settings):
    tests = [('example.jpg', 'original/example.jpg'),
             ('test/example.jpg', 'test/original/example.jpg'),
             ('test/t/example.jpg', 'test/t/original/example.jpg')]
    for src, ref in tests:
        assert get_orig(settings, src) == ref


def test_img_sizes(tmpdir):
    """Test that image size is swaped if needed."""

    conf = tmpdir.join('sigal.conf.py')
    conf.write("""# -*- coding: utf-8 -*-

thumb_size = (150, 200)
""")

    settings = read_settings(str(conf))
    assert settings['thumb_size'] == (200, 150)


def test_theme_path(tmpdir):
    """Test that image size is swaped if needed."""

    tmpdir.join('theme').mkdir()
    conf = tmpdir.join('sigal.conf.py')
    conf.write("""# -*- coding: utf-8 -*-

theme = 'theme'
""")

    settings = read_settings(str(conf))
    assert settings['theme'] == tmpdir.join('theme')
