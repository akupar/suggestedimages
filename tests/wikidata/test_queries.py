import pytest

from suggestedimages.wikidata.queries import *




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
