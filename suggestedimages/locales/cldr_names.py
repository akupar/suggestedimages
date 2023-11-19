import langcodes

class LanguageNames:
    def __init__(self, lang, custom_names):
        self.lang = lang
        self.custom_names = custom_names

    def __getitem__(self, key):
        return self.custom_names.get(key) \
            or langcodes.Language.get(key).display_name(self.lang)
