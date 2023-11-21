from typing import *

from suggestedimages.util import StrInLanguage
from .util import bind_sparql_query, Identifier


def label_or_alias_capitalized_or_not(label: StrInLanguage, limit=50):
    return bind_sparql_query('''

SELECT DISTINCT ?item WHERE{
  VALUES ?prefLabel {
    %label%
    %label_capitalized%
  }

  ?item rdfs:label|skos:altLabel ?prefLabel .
}

LIMIT %limit%

''',
        label = label,
        label_capitalized = label.capitalize(),
        limit = limit
    )



def property_has_any_of_values(property: str, values: list[str], limit=50):
    return bind_sparql_query('''

SELECT DISTINCT ?item WHERE{
  VALUES ?value {
    %values%
  }
  ?item wdt:%property% ?value .
}

LIMIT %limit%

''',
        property = Identifier(property),
        values = values,
        limit = limit
    )
