import langcodes

class LanguageNames:
    """A utility class to return language names in the language given at initialization.

    Returns language names in language `lang`. By default uses the names given stored in the
    CLDR (https://cldr.unicode.org/) database, but Language names can be overridden if the name used
    in the wiktionary doesn't match the name in the database.
    """

    def __init__(self, lang, custom_names = {}):
        self.lang = lang
        self.custom_names = custom_names

    def __getitem__(self, key):
        return self.custom_names.get(key) \
            or langcodes.Language.get(key).display_name(self.lang)

    def keys(self):
        return sorted(
            set(langcodes.LANGUAGE_ALPHA3.keys())
            | set(self.custom_names.keys())
        )
