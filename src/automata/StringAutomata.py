def StringAutomata(state: str, input: str):
    if (state == 'String' and input == '"'):
        return 'StringComplete';
    if (state == 'StringComplete'):
        return 'StringFinal';
    if (state == 'String' and input == '\n'):
        return 'MalformedString';
    if (state == 'MalformedString' and input == '\n'):
        return 'MalformedStringFinal';
    return 'String';
