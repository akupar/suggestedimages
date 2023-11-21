import re

from suggestedimages.util import StrInLanguage


def check_for_invalid_values(params):
    for value in params.values():
        if type(value) == str and value.find('"') != -1:
            raise Exception(f'Invalid parametre value: "{value}"')


def check_for_extra_keys(query, params):
    for key, value in params.items():
        if query.find("%" + key + "%") == -1:
            raise Exception(f"Parametre {key} not found in query")


def check_for_missing_keys(query, params):
    placeholder_regex = re.compile(r"%([^\d\W][\w_]*)", re.UNICODE)

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
        if query.find("%" + key + "%") == -1:
            raise Exception(f"Parametre {key} not found in query")

        query = replace_placeholders(query, key, value)

    return query


def replace_placeholders(query, key, value):
    if type(value) == str:
        return query.replace("%" + key + "%", f'"{value}"')
    elif type(value) == StrInLanguage:
        return query.replace("%" + key + "%", f'"{value.text}"@{value.language}')
    elif type(value) in [int, float]:
        return query.replace("%" + key + "%", str(value))
    elif type(value) == Identifier:
        return query.replace("%" + key + "%", str(value))
    elif type(value) == list:
        return replace_list_placeholders(query, key, value)

    raise NotImplementedError(f'Type: {type(value)}')



def replace_list_placeholders(query, key, list_value):
    assert type(list_value) == list, f"not a list: {list_value}"

    if len(list_value) == 0:
        # Not sure what should happen here.
        raise NotImplementedError(f"Don't know what to do with empty list")

    item_type = type(list_value[0])

    if not all(type(member) == item_type for member in list_value):
        raise Exception(f'All members of a list must have the same type: {list_value}')

    if item_type == str:
        return query.replace("%" + key + "%", " ".join(f'"{member}"' for member in list_value))

    raise NotImplementedError(f'Got list of type {item_type}')
