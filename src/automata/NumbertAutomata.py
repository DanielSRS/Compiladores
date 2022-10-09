import re

def NumbertAutomata(state: str, input: str):
    if (state == 'Number' and re.match(r'\d', input)):
        return 'Number'
    if (state == 'Number' and input == '.'):
        return 'FPNumber'
    if (state == 'FPNumber' and re.match(r'\d', input)):
        return 'FPNumberComplete'
    if (state == 'FPNumberComplete' and re.match(r'\d', input)):
        return 'FPNumberComplete'
    if (state == 'FPNumberComplete' and not re.match(r'\d', input)):
        return 'NumberFinal'
    if (state == 'FPNumber' and not re.match(r'\d', input)):
        return 'MalformedNumberFinal'
    if (state == 'Number' and not (input == ' ' or input == '-' or input == '\t')):
        return 'NumberFinal'
    if (state == 'Number' and (input == ' ' or input == '-' or input == '\t')):
        return 'NumberFinalInPossibleOperation'
    if (state == 'NumberFinalInPossibleOperation' and (input == ' ' or input == '\t')):
        return 'NumberFinalInPossibleOperation_'
    if (state == 'NumberFinalInPossibleOperation_' and (input == ' ' or input == '\t')):
        return 'NumberFinalInPossibleOperation_'
    if (state == 'NumberFinalInPossibleOperation' and input == '-'):
        return 'PossibleArithmeticMinus'
    if (state == 'NumberFinalInPossibleOperation_' and input == '-'):
        return 'PossibleArithmeticMinus'
    if (state == 'NumberFinalInPossibleOperation'):
        return 'InitialState'
    if (state == 'NumberFinalInPossibleOperation_'):
        return 'InitialState'
    else:
        return 'NumberFinal'
