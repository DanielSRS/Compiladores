import re

def ArithmeticOperatorAutomata(state: str, input: str):
    if (state == 'Arithmetic' and input == '+'):
        return 'DoubleArithmeticOperator'
    if (state == 'DoubleArithmeticOperator'):
        return 'ArithmeticOperatorFinal'
    if (state == 'Arithmetic*'):
        return 'ArithmeticOperatorFinal'
    if (state == 'Arithmetic-' and input == '-'):
        return 'DoubleArithmeticOperator'
    if (state == 'DoubleArithmeticOperator'):
        return 'ArithmeticOperatorFinal'
    if (state == 'Arithmetic-' and input == ' '):
        return 'ArithmeticPossibleNROorART'
    if (state == 'Arithmetic-' and re.match(r'\d', input)):
        return 'Number'
    if (state == 'ArithmeticPossibleNROorART' and re.match(r'\d', input)):
        return 'Number'
    if (state == 'ArithmeticPossibleNROorART' and input == ' '):
        return 'ArithmeticPossibleNROorART'
    if (state == 'ArithmeticPossibleNROorART'):
        return 'ArithmeticOperatorFinal'
    if (state == 'PossibleArithmeticMinus' and input == ' ' or input == '\t'):
        return 'PossibleArithmeticMinus'
    if (state == 'PossibleArithmeticMinus' and re.match(r'\d', input)):
        return 'ArithmeticOperatorFinal'
    if (state == 'PossibleArithmeticMinus'):
        return 'GoBack'
    return 'ArithmeticOperatorFinal';
