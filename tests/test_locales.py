import pytest

from suggestedimages.localization import *


def test_Locale():
    test = Locale()
    assert test.wikt == None
    assert test.language == 'en'
    assert test.module is None

    test = Locale('fi')
    assert test.wikt == 'fi'
    assert test.language == 'fi'
    assert test.module is not None

    test = Locale('simple')
    assert test.wikt == 'simple'
    assert test.language == 'en'
    assert test.module is not None

    with pytest.raises(Exception):
        Locale('this-doesnt-exist')


def test_Locale_language_names():
    test = Locale()
    assert test.language_names['am'] == "Amharic"

    import suggestedimages.localization.locales.fi as fi_locale
    test = Locale('fi')
    assert test.language_names['sv'] == fi_locale.language_names['sv']



def test_language_names():
    from suggestedimages.localization.locales.fi import language_names
    assert language_names['sv'] == 'ruotsi'
