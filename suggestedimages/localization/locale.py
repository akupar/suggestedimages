import os
import langcodes
import importlib

from .list_of_wiktionaries import wiktionary_info
from .language_name_db import LanguageNames

LOCALES_DIR = os.path.join(os.path.dirname(__file__), 'locales')


class Locale:

    @staticmethod
    def list_locales():
        return [
            wiktionary_info[filename.removesuffix('.py')] \
            for filename in os.listdir(LOCALES_DIR) \
            if filename.endswith('.py')
        ]

    def __init__(self, wikt=None):
        self.wikt = wikt

        if wikt and wikt not in wiktionary_info:
            raise Exception(f'No such wiktionary: {wikt}')

        info = wiktionary_info.get(wikt)
        self.language = info.language_code if info else 'en'
        self.name = info.local_name if info else '<not set>'

        if wikt is None:
            self.module = None
        else:
            try:
                self.module = importlib.import_module(f'suggestedimages.localization.locales.{wikt}')
            except:
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
            return LanguageNames('en')
        return self.module.language_names

    @property
    def is_localized(self):
        return self.module is not None or self.language == 'en'
