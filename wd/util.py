import re
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
        return type(other) == type(self) \
            and self.language == other.language \
            and self.text == other.text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'"{self.text}"@{self.language}'


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


def check_for_invalid_values(params):
    for value in params.values():
        if type(value) == str and value.find('"') != -1:
            raise Exception(f'Invalid parametre value: "{value}"')


def check_for_extra_keys(query, params):
    for key, value in params.items():
        if query.find("{{" + key + "}}") == -1:
            raise Exception(f"Parametre {key} not found in query")


def check_for_missing_keys(query, params):
    placeholder_regex = re.compile(r"\{\{([^\d\W]\w*)\}\}", re.UNICODE)

    for name in re.findall(placeholder_regex, query):
        if name not in params:
            raise Exception(f"Placeholder {name} not given a value")


class Identifier:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


def bind_sparql_query(query, **params):
    check_for_invalid_values(params)
    check_for_extra_keys(query, params)
    check_for_missing_keys(query, params)

    for key, value in params.items():
        if query.find("{{" + key + "}}") == -1:
            raise Exception(f"Parametre {key} not found in query")

        if type(value) == str:
            query = query.replace("{{" + key + "}}", f'"{value}"')
        elif type(value) in [int, float]:
            query = query.replace("{{" + key + "}}", str(value))
        elif type(value) == Identifier:
            query = query.replace("{{" + key + "}}", str(value))
        else:
            raise Exception(f'Invalid type: {str(value)}')

    return query
