import langcodes
import importlib

from .list_of_wiktionaries import language_of_wiktionary


class DefaultLanguageNames:
    def __getitem__(self, key):
        return langcodes.Language.get(key).display_name()


class Locale:
    def __init__(self, wikt=None):
        self.wikt = wikt

        if wikt and wikt not in language_of_wiktionary:
            raise Exception(f'No such wiktionary: {wikt}')
        else:
            self.language = language_of_wiktionary.get(wikt, 'en')

        try:
            self.module = importlib.import_module(f'suggestedimages.locales.{wikt}')
        except ImportError:
            self.module = None

    def __repr__(self):
        return f"Locale({self.wikt}, language={self.language})"

    def __getitem__(self, key):
        if not self.module:
            return key

        return self.module.texts.get(key, key)

    def format_image(self, name, caption):
        if name.startswith('File:'):
            name = name[len('File:'):]
        return f"[[{self['File']}:{name}|{self['thumb']}|{caption}]]"

    @property
    def language_names(self):
        if not self.module or not self.module.language_names:
            return DefaultLanguageNames()
        return self.module.language_names
