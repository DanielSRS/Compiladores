def getTokenTypeFromState(state: str):
    stateToTokenType = {
        'DelimiterFinal': 'DEL',
        'MalformedStringFinal': 'CMF',
        'StringFinal': 'CAC',
        'LineCommentFinal': 'COM',
        'BlockCommentFinal': 'CMB',
        'ArithmeticFinal': 'ART',
        'LogicalOperatorFinal': 'LOG',
        'MalformedTokenFinal': 'TMF',
        'RelationalOperatorFinal': 'REL',
        'ArithmeticOperatorFinal': 'ART',
        'NumberFinal': 'NRO',
        'MalformedNumber': 'NMF',
        'MalformedNumberFinal': 'NMF',
        'IdentifierFinal': 'IDE',
    }
    return stateToTokenType.get(state, 'None');
