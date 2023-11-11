import pprint
import re

def uppercase_first(string):
    return string[0].upper() + string[1:]

def pretty_print(variable):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(variable)


class StrInLanguage:
    """A string with associated language."""

    def __init__(self, text: str, lang: str=None):
        self.text = str(text)
        self.language = lang

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'"{self.text}"@{self.language}'



if __name__ == "__main__":
    word = StrInLanguage('kissa', lang='fi')
    print(word, str(word), repr(word))
