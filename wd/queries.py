from .util import bind_sparql_query, Identifier

def label_or_alias_capitalized_or_not(text, language, limit=50):
    return bind_sparql_query('''
SELECT distinct ?item ?itemLabel ?itemDescription WHERE{
  VALUES ?prefLabel {
    {{text}}@{{language}}
    {{text_capitalized}}@{{language}}
  }

  ?item rdfs:label|skos:altLabel ?prefLabel
}

LIMIT {{limit}}
''',
        text = text,
        text_capitalized = text.capitalize(),
        language = Identifier(language),
        limit = 50
    )
