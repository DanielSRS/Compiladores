import re
from filesystem import ResTokenList, Token, TokenListPerFile, listDirFiles, readFileLines

LETRA = re.compile(r'/[a-zA-Z]+/g');
DIGITO = re.compile(r'/\d/g');


def onReadLine(line: str, lineNumber: int, initialState: str, overflow: str) -> ResTokenList:
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

def hasNonASCII(s: str):
    count = 0;
    for char in s:
        if (ord(char) < 32 or ord(char) > 126):
            count = count + 1;
    if (count > 0):
        return True;
    return False

def findTokensInString(line: str, lineCount: int, initialState: str, overflow: str) -> ResTokenList:
  lineLength: int = len(line);
  tokenStartIndex: int = 0;
  currentIndex: int = 0;
  currentState: str = initialState;
  tokensFoundInThisLine: list[Token] = [];
  tokenOverflow: str = overflow if initialState == '8' else '';

  exitLoop = False;

  while (not exitLoop and currentIndex < lineLength):
    if (currentState == '0'):
        if (line[currentIndex] == '/'):
            currentIndex = currentIndex + 1;
            currentState = '2';
        elif (isDelimiter(line[currentIndex])):
            t = Token('DEL', lineCount, currentIndex, currentIndex + 1, line[currentIndex:currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
        elif (re.match( r'[a-zA-Z]+', line[currentIndex])):
            currentState = '5';
            tokenStartIndex = currentIndex;
            if(currentIndex + 1 >= lineLength):
                atEndOfLine = line[tokenStartIndex:]
                if (isReserved(line[tokenStartIndex: currentIndex])):
                    t = Token('PRE', lineCount, tokenStartIndex, currentIndex, atEndOfLine);
                else:
                    t = Token('IDE', lineCount, tokenStartIndex, currentIndex, atEndOfLine);
                tokensFoundInThisLine.append(t);
                currentState = '0';
                currentIndex = currentIndex + 1;
            else:
                currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '"'):
            tokenStartIndex = currentIndex;
            currentIndex = currentIndex + 1;
            currentState = '6';
        elif (line[currentIndex] == '&'):
            currentIndex = currentIndex + 1;
            currentState = '14';
        elif (line[currentIndex] == '|'):
            currentIndex = currentIndex + 1;
            currentState = '16';
        elif (line[currentIndex] == '!'):
            currentIndex = currentIndex + 1;
            currentState = '12';
        elif (line[currentIndex] == '=' or line[currentIndex] == '<' or line[currentIndex] == '>'):
            currentIndex = currentIndex + 1;
            currentState = '18';
        elif (line[currentIndex] == '+'):
            currentIndex = currentIndex + 1;
            currentState = '19';
        elif (line[currentIndex] == '*'):
            t = Token('ART', lineCount, currentIndex, currentIndex + 1, line[currentIndex:currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentIndex = currentIndex + 1;
            currentState = '0';
        elif (line[currentIndex] == '-'):
            if (line[currentIndex + 1] == '-'):
                t = Token('ART', lineCount, currentIndex, currentIndex + 2, line[currentIndex:currentIndex + 2]);
                tokensFoundInThisLine.append(t);
                currentIndex = currentIndex + 2;
                currentState = '0';
            else:
                tokenStartIndex = currentIndex;
                currentIndex = currentIndex + 1;
                currentState = '20';
        elif (re.match(r'\d', line[currentIndex])):
            tokenStartIndex = currentIndex;
            currentIndex = currentIndex + 1;
            currentState = '21';
        elif(line[currentIndex] == ' ' or line[currentIndex] == '\t' or line[currentIndex] == '\n'):
            currentIndex = currentIndex + 1;
            currentState = '0';
        else:
            mlkmk = line[currentIndex];
            t = Token('TMF', lineCount, currentIndex, currentIndex, mlkmk);
            tokensFoundInThisLine.append(t);
            currentIndex = currentIndex + 1;
            currentState = '0';
    elif(currentState == '2'):
        if (line[currentIndex] == '*'):
            currentState = '8';
            tokenStartIndex = currentIndex - 1; # considerando a barra anterior
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '/'):
            t = Token('COM', lineCount, currentIndex, lineLength - 1, line[currentIndex - 1: -1]);
            #tokensFoundInThisLine.append(t);
            exitLoop = True;
            currentIndex = lineLength - 1;
            currentState = '0';
        else:
            t = Token('ART', lineCount, currentIndex -1, currentIndex, line[currentIndex - 1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
    elif(currentState == '5'):
        if(currentIndex + 1 >= lineLength):
            atEndOfLine = line[tokenStartIndex:]
            if (isReserved(line[tokenStartIndex: currentIndex])):
                t = Token('PRE', lineCount, tokenStartIndex, currentIndex, atEndOfLine);
            else:
                t = Token('IDE', lineCount, tokenStartIndex, currentIndex, atEndOfLine);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            tokenStartIndex = 0;
        elif (line[currentIndex] == '_' or re.match(r'[a-zA-Z]+', line[currentIndex]) or re.match(r'\d', line[currentIndex])):
            currentIndex = currentIndex + 1;
        else:
            ideToken = line[tokenStartIndex: currentIndex]
            if (isReserved(line[tokenStartIndex: currentIndex])):
                t = Token('PRE', lineCount, tokenStartIndex, currentIndex, ideToken);
            else:
                t = Token('IDE', lineCount, tokenStartIndex, currentIndex, ideToken);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            tokenStartIndex = 0;
    elif(currentState == '6'):
        if (line[currentIndex] == '"'):
            stoken = line[tokenStartIndex: currentIndex + 1];
            if (hasNonASCII(stoken)):
                t = Token('CMF', lineCount, tokenStartIndex, currentIndex, stoken);
            else:
                t = Token('CAC', lineCount, tokenStartIndex, currentIndex, stoken);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            tokenStartIndex = 0;
            currentIndex = currentIndex + 1;
        elif(line[currentIndex] == '\n'):
            t = Token('CMF', lineCount, tokenStartIndex, lineLength, line[tokenStartIndex: lineLength - 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            tokenStartIndex = 0;
            currentIndex = currentIndex + 1;
        else:
            currentIndex = currentIndex + 1;
    elif(currentState == '8'):
        if (line[currentIndex] == '*'):
            currentState = '10';
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '\n' or currentIndex == lineLength -1):
            l = line.replace('\n', '');
            if (line != '\n'):
                tokenOverflow = tokenOverflow + l[tokenStartIndex: len(l)];
            currentIndex = currentIndex + 1;
        else:
            currentIndex = currentIndex + 1;
    elif(currentState == '10'):
        if (line[currentIndex] == '/'):
            t = Token('COM', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            #tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
        else:
            currentState = '8';
            currentIndex = currentIndex + 1;
    elif(currentState == '14'):
        if (line[currentIndex] == '&'):
            t = Token('LOG', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
        else:
            t = Token('TMF', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentIndex = currentIndex + 1;
            currentState = '0';
    elif(currentState == '16'):
        if (line[currentIndex] == '|'):
            t = Token('LOG', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
        else:
            t = Token('TMF', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentIndex = currentIndex + 1;
            currentState = '0';
    elif(currentState == '12'):
        if (line[currentIndex] == '='):
            t = Token('REL', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
        else:
            t = Token('LOG', lineCount, currentIndex -1, currentIndex, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
    elif(currentState == '18'):
        if (line[currentIndex] == '='):
            t = Token('REL', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
        else:
            t = Token('REL', lineCount, currentIndex -1, currentIndex, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
    elif(currentState == '19'):
        if (line[currentIndex] == '+'):
            t = Token('ART', lineCount, currentIndex -1, currentIndex + 1, line[currentIndex -1: currentIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
            currentIndex = currentIndex + 1;
        else:
            t = Token('ART', lineCount, currentIndex -1, currentIndex, line[currentIndex -1: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
    elif(currentState == '20'):
        if (re.match(r'\d', line[currentIndex])):
            currentState = '21';
        elif (line[currentIndex] == ' '):
            currentIndex = currentIndex + 1;
        else:
            t = Token('ART', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
    elif(currentState == '21'):
        if(currentIndex + 1 >= lineLength):
            l = line[tokenStartIndex:]
            if (l[len(l) - 1] == '\n'):
                l = l
                #l = l[ :- 1]
            t = Token('NRO', lineCount, tokenStartIndex, currentIndex, l);
            tokensFoundInThisLine.append(t);
            currentIndex = currentIndex + 1;
        elif (re.match(r'\d', line[currentIndex])):
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '.'):
            currentState = '22';
            currentIndex = currentIndex + 1;
        else:
            t = Token('NRO', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            if (line[currentIndex] == ' ' or line[currentIndex] == '-' or line[currentIndex] == '\t'):
                currentState = '24';
            else:
                currentState = '0';
    elif(currentState == '22'):
        if (re.match(r'\d', line[currentIndex])):
            currentIndex = currentIndex + 1;
            currentState = '23';
        else:
            t = Token('NMF', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
    elif(currentState == '23'):
        if (re.match(r'\d', line[currentIndex])):
            currentIndex = currentIndex + 1;
        else:
            t = Token('NRO', lineCount, tokenStartIndex, currentIndex, line[tokenStartIndex: currentIndex]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
    elif(currentState == '24'):
        if (line[currentIndex] == ' ' or line[currentIndex] == '\t'):
            currentIndex = currentIndex + 1;
        elif (line[currentIndex] == '-'):
            tokenStartIndex = currentIndex;
            currentIndex = currentIndex + 1;
            currentState = '25';
        else:
            currentState = '0';
    elif(currentState == '25'):
        if (line[currentIndex] == ' ' or line[currentIndex] == '\t'):
            currentIndex = currentIndex + 1;
        elif (re.match(r'\d', line[currentIndex])):
            t = Token('ART', lineCount, tokenStartIndex, tokenStartIndex + 1, line[tokenStartIndex: tokenStartIndex + 1]);
            tokensFoundInThisLine.append(t);
            currentState = '0';
        else:
            currentIndex = tokenStartIndex;
            currentState = '0';
    else:
        exitLoop = True;

  if (currentState != '8'):
    currentState = '0';
  return ResTokenList(currentState, tokenStartIndex, lineCount, tokenOverflow, tokensFoundInThisLine);


def isError(err: str):
    errors = {'CMF', 'CoMF', 'NMF', 'IMF', 'TMF'}
    if err in errors:
        return True;
    return False

def orderTokens(tk: Token):
    if (isError(tk.token)):
        return 1;
    return 0;

def errorCount(tk: 'list[Token]'):
    ec = 0
    for t in tk:
        if (isError(t.token)):
            ec = ec + 1;
    return ec;


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
    tokensFound.sort(key=orderTokens);

    errorsNum = errorCount(tokensFound);

    # salva as informaações em um arquivo
    #print(tabulate(tokensFound, headers=['token', 'line', 'tokeStartIndex', 'tokenEndIndex', 'value']));
    tokenListPerFile[filename] = [];
    for token in tokensFound:
        formatedOutput = '{0:02d} {1:s} {2:s}\n'.format(token.line, token.token, token.value.replace('\n', ''));
        #print(formatedOutput);
        tokenListPerFile[filename].append(formatedOutput);

    if(errorsNum > 0):
        # Se houver erros, adiciona uma quebra de linha antes da lista de erros
        tokenListPerFile[filename].insert(-errorsNum, '\n');

    lastTokenString = tokenListPerFile[filename][-1];
    if (lastTokenString[len(lastTokenString) - 1] == '\n'):
        tokenListPerFile[filename][-1] = tokenListPerFile[filename][-1][0:len(lastTokenString) - 1]; # temove quebra de linha do ultimo item

    outputFile = open('saida/' + filename, 'w');
    outputFile.writelines(tokenListPerFile[filename])
    source_file.close();
    outputFile.close();
  return;

lexico();