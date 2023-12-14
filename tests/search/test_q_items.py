import pytest

from suggestedimages.search.q_items import *
from suggestedimages.util import StrInLanguage



def test_yield_external_results():
    # https://www.wikidata.org/wiki/Q20793
    CORRECT_ID = 'Q20793'

    searched_word = StrInLanguage('eurooppalainen lyhytkarva', 'fi')
    results = list(yield_external_results(searched_word))

    assert len(results) == 1
    assert results[0].id == CORRECT_ID
