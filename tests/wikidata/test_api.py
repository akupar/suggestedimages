import pytest

from suggestedimages.wikidata.api import *


def test_spaced():
    assert spaced() == ''
    assert spaced(None, None, None) == ''
    assert spaced('a', 'b', 'c', 'd') == 'a b c d'
    assert spaced('a', None, 'c', 'd') == 'a c d'
    assert spaced(None, 'b', 'c', 'd') == 'b c d'
    assert spaced('a', 'b', 'c', None) == 'a b c'
    assert spaced('a', None, None, 'd') == 'a d'


def test_build_composite_description():
    assert build_composite_description('cat', None, None, None) == 'cat'
    assert build_composite_description('cat', None, None, 'an animal') == 'cat: an animal'
    assert build_composite_description('cat', ['domestic cat'], None, 'an animal') \
        == 'cat (domestic cat): an animal'

    assert build_composite_description('kissa', None, 'cat', None) == 'kissa [= cat]'
    assert build_composite_description('kissa', None, 'cat', 'an animal') == 'kissa [= cat]: an animal'

    assert build_composite_description('kissa', ['kotikissa'], 'cat', 'an animal') \
        == 'kissa (kotikissa) [= cat]: an animal'

    assert build_composite_description('kissa', ['kotikissa', 'kesykissa'], 'cat', 'an animal') \
        == 'kissa (kotikissa, kesykissa) [= cat]: an animal'
