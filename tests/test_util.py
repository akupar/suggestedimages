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



def test_GeneratorCache_case_default_cache_time_is_one_day():
    cache = GeneratorCache()
    assert cache.keep_time == 60 * 60 * 24


def test_GeneratorCache_case_deletes_outdated_items():
    import time
    cache = GeneratorCache(1.0)
    cache['test1'] = 'x'
    time.sleep(0.5)
    cache['test2'] = 'y'

    assert cache['test1'] == 'x'
    assert cache['test2'] == 'y'

    time.sleep(0.6)
    assert cache['test2'] == 'y'

    with pytest.raises(KeyError):
        x = cache['testi1']


def test_GeneratorCache_case_doesnt_delete_outdated_items_if_new_items_are_not_added():
    import time
    cache = GeneratorCache(1.0)
    cache['test1'] = 'x'
    time.sleep(0.5)

    assert cache['test1'] == 'x'

    time.sleep(0.6)

    assert cache['test1'] == 'x'
