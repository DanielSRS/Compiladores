def CommentAutomata(state: str, input: str):
    if (state == 'PossibleComment' and not (input == '*' or input == '/')):
        return 'ArithmeticFinal'
    if (state == 'PossibleComment' and input == '*'):
        return 'BlockComment'
    if (state == 'PossibleComment' and input == '/'):
        return 'LineComment'
    if (state == 'LineComment' and input == '\n'):
        return 'LineCommentFinal'
    if (state == 'BlockComment' and input == '\n'):
        return 'BlockCommentOverflow'
    if (state == 'LineComment'):
        return 'LineComment'
    if (state == 'BlockComment' and input == '*'):
        return 'ClosingBlockComment'
    if (state == 'ClosingBlockComment' and input == '/'):
        return 'BlockCommentComplete'
    if (state == 'BlockCommentComplete'):
        return 'BlockCommentFinal'
    if (state == 'ClosingBlockComment' and not input == '/'):
        return 'BlockComment'
    if (state == 'BlockComment'):
        return 'BlockComment'
    return state + 'Error:_' + input;
