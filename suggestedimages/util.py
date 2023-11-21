import re
import pprint


def pretty_print(variable):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(variable)


class StrInLanguage:
    """A string with an associated language."""

    def __init__(self, text: str, lang: str=None):
        self.text = str(text)
        self.language = lang

    def __eq__(self, other):
        return type(other) == type(self) \
            and self.language == other.language \
            and self.text == other.text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'"{self.text}"@{self.language}'

    def capitalize(self):
        return StrInLanguage(self.text.capitalize(), self.language)


class StrInLanguages:
    """Utility class to extract StrInLanguage from a dict
    """
    def __init__(self, dictlike):
        self.__dict = dictlike

    def __eq__(self, other):
        return type(other) == type(self) \
            and self.__dict == other.__dict

    def keys(self):
        return self.__dict.keys()

    def get(self, *langs):
        """Get value in first language in langs, that is found"""
        for lang in langs:
            value = self.__get(lang)
            if value:
                return value
        return None

    def __get(self, lang):
        if lang not in self.__dict:
            return None

        value = self.__dict[lang]
        if type(value) not in [str, list]:
            raise NotImplementedError

        if type(value) == str:
            return StrInLanguage(value, lang=lang)

        if not all(type(item) == str for item in value):
            raise Exception('Value must be str or list of str')

        return [StrInLanguage(item, lang=lang) for item in value]


    def add(self, item: StrInLanguage):
        lang = item.language

        if lang in self.__dict:
            raise Exception(f'Language {lang} already exists')

        self.__dict[lang] = item.text

        print(self.__dict)
