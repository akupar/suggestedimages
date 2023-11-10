import pprint

def uppercase_first(string):
    return string[0].upper() + string[1:]

def pretty_print(variable):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(variable)
