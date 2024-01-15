import pytest

from suggestedimages.util import *




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
