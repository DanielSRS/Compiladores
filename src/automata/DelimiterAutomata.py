def DelimiterAutomata(state: str, input: str):
    if (state == 'DelimiterFinal'):
        return 'DelimiterFinal';
    if (state == 'Delimiter'):
        return 'DelimiterFinal';
    return state + 'Error:_' + input;
