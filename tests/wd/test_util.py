import pytest

from wd.util import *

def test_spaced():
    assert spaced() == ''
    assert spaced(None, None, None) == ''
    assert spaced('a', 'b', 'c', 'd') == 'a b c d'
    assert spaced('a', None, 'c', 'd') == 'a c d'
    assert spaced(None, 'b', 'c', 'd') == 'b c d'
    assert spaced('a', 'b', 'c', None) == 'a b c'
    assert spaced('a', None, None, 'd') == 'a d'


def test_build_tooltip():
    assert build_tooltip('cat', None, None, None) == 'cat'
    assert build_tooltip('cat', None, None, 'an animal') == 'cat: an animal'
    assert build_tooltip('cat', ['domestic cat'], None, 'an animal') \
        == 'cat (domestic cat): an animal'

    assert build_tooltip('kissa', None, 'cat', None) == 'kissa [= cat]'
    assert build_tooltip('kissa', None, 'cat', 'an animal') == 'kissa [= cat]: an animal'

    assert build_tooltip('kissa', ['kotikissa'], 'cat', 'an animal') \
        == 'kissa (kotikissa) [= cat]: an animal'

    assert build_tooltip('kissa', ['kotikissa', 'kesykissa'], 'cat', 'an animal') \
        == 'kissa (kotikissa, kesykissa) [= cat]: an animal'






def test_StrsInLanguage():
    assert StrInLanguages({ 'en': 'cat', 'fi': 'kissa' }).get('fi') \
        == StrInLanguage('kissa', lang='fi')

    assert StrInLanguages({ 'en': 'cat', 'fi': 'kissa' }).get('fi', 'en') \
        == StrInLanguage('kissa', lang='fi')

    assert StrInLanguages({ 'en': 'cat', 'fi': 'kissa' }).get('es', 'en') \
        == StrInLanguage('cat', lang='en')

    assert StrInLanguages({ 'en': ['cat', 'domestic cat'], 'fi': ['kissa', 'kotikissa'] }).get('fi') \
        == [StrInLanguage('kissa', lang='fi'), StrInLanguage('kotikissa', lang='fi')]

    with pytest.raises(NotImplementedError):
        StrInLanguages({ 'en': 3, 'fi': 4 }).get('fi')

    with pytest.raises(Exception):
        StrInLanguages({ 'en': [2, 3], 'fi': [4, 5] }).get('fi')


    x = StrInLanguages({ 'en': 'cat', 'fi': 'kissa' })
    x.add(StrInLanguage('gato', lang='es'))
    assert x == StrInLanguages({ 'en': 'cat', 'fi': 'kissa', 'es': 'gato' })



def test_bind_sparql_query():
    assert bind_sparql_query("abc") == "abc"

    assert bind_sparql_query("{{x}}", x=1) == "1"
    assert bind_sparql_query("{{x}}", x=1.2) == "1.2"
    assert bind_sparql_query("{{x}}", x='word') == '"word"'
    assert bind_sparql_query("{{x}}", x=Identifier('fi')) == 'fi'

    assert bind_sparql_query("{{x}} = {{x}}", x=1) == "1 = 1"
    assert bind_sparql_query("{{x}} + {{y}} = {{z}}", x=1, y=2, z=3) == "1 + 2 = 3"



    with pytest.raises(Exception):
        bind_sparql_query("{{x}}", x='"cat"')

    with pytest.raises(Exception):
        bind_sparql_query("{{x}} {{y}}", x='1')

    with pytest.raises(Exception):
        bind_sparql_query("{{x}}", x='1', y="2")
