import re

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
