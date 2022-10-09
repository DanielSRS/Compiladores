def LogicalOperatorAutomata(state: str, input: str):
    if (state == 'PossibleLogical&&' and input == '&'):
        return 'DoubleLogicalOperator'
    if (state == 'DoubleLogicalOperator'):
        return 'LogicalOperatorFinal'
    if (state == 'PossibleLogical||' and input == '|'):
        return 'DoubleLogicalOperator'
    if (state == 'PossibleLogical!' and not input == '='):
        return 'LogicalOperatorFinal'
    if (state == 'PossibleLogical!' and input == '='):
        return 'DoubleRelationalOperator'
    return 'MalformedToken';
