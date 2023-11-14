import pprint


def pretty_print(variable):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(variable)

def spaced(*args):
    return " ".join(str(arg) for arg in args if arg != None)

def build_tooltip(label, aliases, translation, description):
    return spaced((label if label else None),
                  ((f"({', '.join([str(alias) for alias in aliases])})") if aliases else None),
                  ((f"[= {translation}]") if translation else None)) \
                  + ((f": {description}") if description else "")

class StrInLanguage:
    """A string with an associated language."""

    def __init__(self, text: str, lang: str=None):
        self.text = str(text)
        self.language = lang

    def __eq__(self, other):
        return self.language == other.language\
            and self.text == other.text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'"{self.text}"@{self.language}'
