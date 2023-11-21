"""Handler for Finto API (https://finto.fi/en/)
"""

import requests

from .base import ExternalApi


class Finto(ExternalApi):
    def __init__(self, vocab, lang):
        self.vocab = vocab
        self.lang = lang

    def call_api(self, word):
        response = requests.get(
            'http://api.finto.fi/rest/v1/search',
            params={
                'vocab': self.vocab,
                'lang': self.lang,
                'query': word
            }
        )

        return response.json()

        # Example response:
        # {   '@context': {   '@language': 'fi',
        #                     'altLabel': 'skos:altLabel',
        #                     'hiddenLabel': 'skos:hiddenLabel',
        #                     'isothes': 'http://purl.org/iso25964/skos-thes#',
        #                     'onki': 'http://schema.onki.fi/onki#',
        #                     'prefLabel': 'skos:prefLabel',
        #                     'results': {'@container': '@list', '@id': 'onki:results'},
        #                     'skos': 'http://www.w3.org/2004/02/skos/core#',
        #                     'type': '@type',
        #                     'uri': '@id'},
        #     'results': [   {   'lang': 'fi',
        #                        'localname': 'p24275',
        #                        'prefLabel': 'eurooppalainen lyhytkarva',
        #                        'type': [   'skos:Concept',
        #                                    'http://www.yso.fi/onto/yso-meta/Concept'],
        #                        'uri': 'http://www.yso.fi/onto/yso/p24275',
        #                        'vocab': 'yso'}],
        #     'uri': ''}



if __name__ == "__main__":
    import sys
    from suggestedimages.util import pretty_print

    yso = Finto('yso', sys.argv[1])
    pretty_print(yso[sys.argv[2]])
