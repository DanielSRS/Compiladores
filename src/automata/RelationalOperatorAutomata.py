def RelationalOperatorAutomata(state: str, input: str):
    if (state == 'Relational' and input == '='):
        return 'DoubleRelationalOperator'
    if (state == 'DoubleRelationalOperator'):
        return 'RelationalOperatorFinal'
    return 'RelationalOperatorFinal';
