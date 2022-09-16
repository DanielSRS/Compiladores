import re
from filesystem import ResTokenList, Token, TokenListPerFile, listDirFiles, readFileLines

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
            t = Token('DEL', lineCount, currentIndex, currentIndex + 1, line[currentIndex:currentIndex + 1]);
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
        elif (line[currentIndex] == '&'):
            currentIndex = currentIndex + 1;
            currentState = 14;
        elif (line[currentIndex] == '|'):
            currentIndex = currentIndex + 1;
            currentState = 16;
        elif (line[currentIndex] == '!'):
            currentIndex = currentIndex + 1;
            currentState = 12;
        elif (line[currentIndex] == '=' or line[currentIndex] == '<' or line[currentIndex] == '>'):
            currentIndex = currentIndex + 1;
            currentState = 18;
        elif (line[currentIndex] == '+'):
            currentIndex = currentIndex + 1;
            currentState = 19;
        elif (line[currentIndex] == '*'):
            t = Token('ART', lineCount, currentIndex, currentIndex + 1, line[currentIndex:currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentIndex = currentIndex + 1;
            currentState = 0;
        elif (line[currentIndex] == '-'):
            if (line[currentIndex + 1] == '-'):
                t = Token('ART', lineCount, currentIndex, currentIndex + 2, line[currentIndex:currentIndex + 2]);
                tokensFoundInThisLine.append(t);
                currentIndex = currentIndex + 2;
                currentState = 0;
            else:
                tokenStartIndex = currentIndex;
                currentIndex = currentIndex + 1;
                currentState = 20;
        elif (re.match(r'\d', line[currentIndex])):
            tokenStartIndex = currentIndex;
            currentIndex = currentIndex + 1;
            currentState = 21;
        else:
            currentIndex = currentIndex + 1;
            currentState = 0;
    elif(currentState == 2):
        if (line[currentIndex] == '*'):
            currentState = 8;
            tokenStartIndex = currentIndex - 1; # considerando a barra anterior
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '/'):
            t = Token('COM', lineCount, currentIndex, lineLength - 1, line[currentIndex - 1: -1]);
            #tokensFoundInThisLine.append(t);
            exitLoop = True;
            currentIndex = lineLength - 1;
            currentState = 0;
        else:
            t = Token('ART', lineCount, currentIndex -1, currentIndex, line[currentIndex - 1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
    elif(currentState == 5):
        if (line[currentIndex] == '_' or re.match(r'[a-zA-Z]+', line[currentIndex]) or re.match(r'\d', line[currentIndex])):
            currentIndex = currentIndex + 1;
        else:
            if (isReserved(line[tokenStartIndex: currentIndex])):
                t = Token('PRE', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            else:
                t = Token('IDE', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            tokenStartIndex = 0;
    elif(currentState == 6):
        if (line[currentIndex] == '"'):
            t = Token('CAC', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            tokenStartIndex = 0;
            currentIndex = currentIndex + 1;
        elif(line[currentIndex] == '\n'):
            t = Token('CMF', lineCount, tokenStartIndex, lineLength, line[tokenStartIndex: lineLength - 1]);
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
            t = Token('COM', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            #tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        else:
            currentIndex = currentIndex + 1;
    elif(currentState == 14):
        if (line[currentIndex] == '&'):
            t = Token('LOG', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        else:
            print('caractere invalido!!')
            currentIndex = currentIndex + 1;
            currentState = 0;
    elif(currentState == 16):
        if (line[currentIndex] == '|'):
            t = Token('LOG', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        else:
            print('caractere invalido!!')
            currentIndex = currentIndex + 1;
            currentState = 0;
    elif(currentState == 12):
        if (line[currentIndex] == '='):
            t = Token('REL', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        else:
            t = Token('LOG', lineCount, currentIndex -1, currentIndex, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
    elif(currentState == 18):
        if (line[currentIndex] == '='):
            t = Token('REL', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        else:
            t = Token('REL', lineCount, currentIndex -1, currentIndex, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
    elif(currentState == 19):
        if (line[currentIndex] == '+'):
            t = Token('ART', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
            currentIndex = currentIndex + 1;
        else:
            t = Token('ART', lineCount, currentIndex -1, currentIndex, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
    elif(currentState == 20):
        if (re.match(r'\d', line[currentIndex])):
            currentState = 21;
        elif (line[currentIndex] == ' '):
            currentIndex = currentIndex + 1;
        else:
            t = Token('ART', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
    elif(currentState == 21):
        if (re.match(r'[a-zA-Z]+', line[currentIndex]) or re.match(r'\d', line[currentIndex])):
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '.'):
            currentIndex = currentIndex + 1;
        else:
            t = Token('NRO', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = 0;
    else:
        exitLoop = True;

  if (currentState != 8):
    currentState = 0;
  return ResTokenList(currentState, tokenStartIndex, lineCount, tokenOverflow, tokensFoundInThisLine);


def lexico():
  source_directory = 'entrada';
  # Get the file handler
  #fhand = open('src/entrada.txt', 'r');
  entry_files: list[str] = listDirFiles(source_directory);

  tokenListPerFile: TokenListPerFile = {}

# para cada arquivo fonte na pasta de entrada
  for filename in entry_files:
    filepath = source_directory + '/' + filename; # define o caminho para o arquivo
    source_file = open(filepath, 'r'); # abre o arquivo
    tokensFound: list[Token] = readFileLines(source_file, onReadLine); # le os arquivos e recupera os token

    # salva as informaações em um arquivo
    #print(tabulate(tokensFound, headers=['token', 'line', 'tokeStartIndex', 'tokenEndIndex', 'value']));
    tokenListPerFile[filename] = [];
    for token in tokensFound:
        formatedOutput = '{0:02d} {1:s} {2:s}\n'.format(token.line, token.token, token.value);
        #print(formatedOutput);
        tokenListPerFile[filename].append(formatedOutput);

    outputFile = open('saida/' + filename, 'w');
    outputFile.writelines(tokenListPerFile[filename])
    source_file.close();
  return;

lexico();