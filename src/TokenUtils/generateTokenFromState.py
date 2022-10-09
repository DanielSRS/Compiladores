from TokenUtils.Token import Token
from TokenUtils.getTokenTypeFromState import getTokenTypeFromState

# verifica se um caractere é uma palavra reservada
def isReserved(identifier: str) -> bool:
    reserved = {'var', 'const', 'struct', 'extends', 'procedure', 'function', 'start', 'return', 'if',
                'else', 'then', 'while', 'read', 'print', 'int', 'real', 'boolean', 'string', 'true', 'false'}
    if identifier in reserved:
        return True
    return False

def hasNonASCII(s: str):
    count = 0;
    for char in s:
        if (ord(char) < 32 or ord(char) > 126):
            count = count + 1;
    if (count > 0):
        return True;
    return False

def generateTokenFromState(state: str, lineNumber: int, lineText: str, tokenStartIndex: int, tokenEndIndex: int) -> Token:
    tokenType = getTokenTypeFromState(state);
    tokenText = lineText[tokenStartIndex:tokenEndIndex];
    if (tokenType == 'IDE'):
        tokenType = 'PRE' if isReserved(tokenText) else 'IDE';
    if (tokenType == 'CAC'):
        tokenType = 'CMF' if hasNonASCII(tokenText) else 'CAC';
    return Token(tokenType, lineNumber, tokenStartIndex, tokenEndIndex, tokenText);
