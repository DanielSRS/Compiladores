import re


def IdendifierAutomata(state: str, input: str):
    isValid = re.match(r'[a-zA-Z]+', input) or re.match(r'\d', input) or input == '_';
    if (state == 'IdentifierFinal'):
        return 'IdentifierFinal';
    if (state == 'Identifier' and isValid):
        return 'Identifier'
    elif (state == 'Identifier' and not isValid):
        return 'IdentifierFinal'
    return state + 'Error:_' + input;
