import pytest

from suggestedimages.wikidata.queries import *



def test_bind_sparql_query_correct_input():
    assert bind_sparql_query("abc") == "abc"

    assert bind_sparql_query("{{x}}", x=1) == "1"
    assert bind_sparql_query("{{x}}", x=1.2) == "1.2"
    assert bind_sparql_query("{{x}}", x='word') == '"word"'
    assert bind_sparql_query("{{x}}", x=Identifier('fi')) == 'fi'
    assert bind_sparql_query("{{x}}", x=["a", "b", "c"]) == '"a" "b" "c"'

    assert bind_sparql_query("{{x}} = {{x}}", x=1) == "1 = 1"
    assert bind_sparql_query("{{x}} + {{y}} = {{z}}", x=1, y=2, z=3) == "1 + 2 = 3"


def test_bind_sparql_raises_on_quotes_in_strings():
    with pytest.raises(Exception):
        bind_sparql_query("{{x}}", x='"cat"')

def test_bind_sparql_raises_on_missing_parametres():
    with pytest.raises(Exception):
        bind_sparql_query("{{x}} {{y}}", x='1')

def test_bind_sparql_raises_on_extra_parametres():
    with pytest.raises(Exception):
        bind_sparql_query("{{x}}", x='1', y="2")

def test_bind_sparql_raises_on_mismatched_list_members():
    with pytest.raises(Exception):
        bind_sparql_query("{{x}}", x=["a", "b", 3])


def test_bind_sparql_raises_not_implemented_on_uknown_types():
    with pytest.raises(NotImplementedError):
        bind_sparql_query("{{x}}", x=[1, 2, 3])

def test_bind_sparql_raises_not_implemented_on_empty_list():
    with pytest.raises(NotImplementedError):
        bind_sparql_query("{{x}}", x=[])
