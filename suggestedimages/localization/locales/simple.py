from ..language_name_db import LanguageNames

class ReturnKeyDict:
    """Returns the key as the value when accessed.
    """

    def __getitem__(self, key):
        return key

    def get(self, key, *args):
        return key


texts = ReturnKeyDict()

language_names = LanguageNames('en')
