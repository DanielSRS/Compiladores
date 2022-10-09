from TokenUtils.Token import Token


def isError(err: str):
    errors = {'CMF', 'CoMF', 'NMF', 'IMF', 'TMF'}
    if err in errors:
        return True;
    return False

def orderTokens(tk: Token):
    if (isError(tk.token)):
        return 1;
    return 0;
  