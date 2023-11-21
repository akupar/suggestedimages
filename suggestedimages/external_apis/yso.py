from typing import *

from .base import ExternalResult, Ref
from .finto import Finto

class YSO(Finto):
    wikidata_property = "P2347"

    def __init__(self, lang):
        super().__init__('yso', lang)


    def get(self, word) -> list[ExternalResult]:
        json_response = self.call_api(word)
        if 'results' not in json_response:
            return []

        return [
            ExternalResult(
                Ref(
                    property=self.wikidata_property,
                    # Wikidata doesn't have the p in the beginning in the identifiers.
                    value=item['localname'].lstrip('p')
                ),
                item['prefLabel'],
                [item['altLabel']] if 'altLabel' in item else []
            ) \
            for item in json_response['results'] \
            # We're only interested in exact maches
            if item['prefLabel'] == word or item.get('altLabel') == word
        ]



if __name__ == "__main__":
    import sys
    from suggestedimages.util import pretty_print

    yso = YSO(sys.argv[1])
    pretty_print(yso[sys.argv[2]])
