from ..cldr_names import LanguageNames

class NopDict:
    def __getitem__(self, key):
        return key

    def get(self, key, *args):
        return key


texts = NopDict()

language_names = LanguageNames('en', {})
