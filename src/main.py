import re
from filesystem import ResTokenList, Token, readFileLines
from tabulate import tabulate

# Get the file handler
fhand = open('src/entrada.txt', 'r')

LETRA = re.compile(r'/[a-zA-Z]+/g');
DIGITO = re.compile(r'/\d/g');


def onReadLine(line: str, lineNumber: int, initialState: int, overflow: str) -> ResTokenList:
    # Se a linha estiver vaxia não fax nada
    tokens = findTokensInString(line, lineNumber, initialState, overflow);
    return tokens;

# verifica se um caractere é um delimitador
def isDelimiter(charactere: str) -> bool:
    delimiters = {'.', ';', ',', '(', ')', '[', ']', '{', '}'}
    if charactere in delimiters:
        return True
    return False

# verifica se um caractere é uma palavra reservada
def isReserved(identifier: str) -> bool:
    reserved = {'var', 'const', 'struct', 'extends', 'procedure', 'function', 'start', 'return', 'if',
                'else', 'then', 'while', 'read', 'print', 'int', 'real', 'boolean', 'string', 'true', 'false'}
    if identifier in reserved:
        return True
    return False

def findTokensInString(line: str, lineCount: int, initialState: int, overflow: str) -> ResTokenList:
  lineLength: int = len(line);
  tokenStartIndex: int = 0;
  currentIndex: int = 0;
  currentState: int = initialState;
  tokensFoundInThisLine: list[Token] = [];
  tokenOverflow: str = overflow;

  exitLoop = False;

  while (not exitLoop and currentIndex < lineLength):
    if (currentState == 0):
        if (line[currentIndex] == '/'):
            currentIndex = currentIndex + 1;
            currentState = 2;
        elif (isDelimiter(line[currentIndex])):
            t = Token('Delimitador', lineCount, currentIndex, currentIndex + 1, line[currentIndex:currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        elif (re.match( r'[a-zA-Z]+', line[currentIndex])):
            currentState = 5;
            tokenStartIndex = currentIndex;
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '"'):
            tokenStartIndex = currentIndex;
            currentIndex = currentIndex + 1;
            currentState = 6;
        else:
            currentIndex = currentIndex + 1;
            currentState = 0;
    elif(currentState == 2):
        if (line[currentIndex] == '*'):
            currentState = 8;
            tokenStartIndex = currentIndex;
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '/'):
            t = Token('Comentario', lineCount, currentIndex, lineLength - 1, line[currentIndex - 1: -1]);
            tokensFoundInThisLine.append(t);
            exitLoop = True;
            currentIndex = lineLength - 1;
            currentState = 0;
        else:
            currentState = 0;
            exitLoop = True;
    elif(currentState == 5):
        if (line[currentIndex] == '_' or re.match(r'[a-zA-Z]+', line[currentIndex]) or re.match(r'\d', line[currentIndex])):
            currentIndex = currentIndex + 1;
        else:
            t = Token('Identificador', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            tokenStartIndex = 0;
    elif(currentState == 6):
        if (line[currentIndex] == '"'):
            t = Token('Cadeia de caracteres', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            tokenStartIndex = 0;
            currentIndex = currentIndex + 1;
        elif(line[currentIndex] == '\n'):
            t = Token('string mal', lineCount, tokenStartIndex, lineLength, line[tokenStartIndex: lineLength]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            tokenStartIndex = 0;
            currentIndex = currentIndex + 1;
        else:
            currentIndex = currentIndex + 1;
    elif(currentState == 8):
        if (line[currentIndex] == '*'):
            currentState = 10;
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '\n' or currentIndex == lineLength -1):
            l = line.replace('\n', '');
            if (line != '\n'):
                tokenOverflow = tokenOverflow + l[tokenStartIndex: len(l)];
            currentIndex = currentIndex + 1;
        else:
            currentIndex = currentIndex + 1;
    elif(currentState == 10):
        if (line[currentIndex] == '/'):
            t = Token('Bloco', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        else:
            currentIndex = currentIndex + 1;
    else:
        exitLoop = True;

  return ResTokenList(currentState, tokenStartIndex, lineCount, tokenOverflow, tokensFoundInThisLine);


def lexico():
  tokensFound: list[Token] = readFileLines(fhand, onReadLine);
  print(tabulate(tokensFound, headers=['token', 'line', 'tokeStartIndex', 'tokenEndIndex', 'value']));
  return;

lexico();