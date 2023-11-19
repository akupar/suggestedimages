from typing import *

from .util import bind_sparql_query, Identifier


def label_or_alias_capitalized_or_not(text: str, language: str, limit=50):
    return bind_sparql_query('''
SELECT DISTINCT ?item WHERE{
  VALUES ?prefLabel {
    {{text}}@{{language}}
    {{text_capitalized}}@{{language}}
  }

  ?item rdfs:label|skos:altLabel ?prefLabel .
}

LIMIT {{limit}}
''',
        text = text,
        text_capitalized = text.capitalize(),
        language = Identifier(language),
        limit = limit
    )



def property_has_any_of_values(property: str, values: list[str], limit=50):
    """Return items where property `property` has any of values `values`.
    """
    return bind_sparql_query('''
SELECT DISTINCT ?item WHERE{
  VALUES ?value {
    {{values}}
  }
  ?item wdt:{{property}} ?value .
}

LIMIT {{limit}}
''',
        property = Identifier(property),
        values = values,
        limit = limit
    )
