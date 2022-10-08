import re
from typing import Callable
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

Automata = Callable[[str, str], str];

def IdendifierAutomata(state: str, input: str):
    isValid = re.match(r'[a-zA-Z]+', input) or re.match(r'\d', input);
    if (state == 'IdentifierFinal'):
        return 'IdentifierFinal';
    if (state == 'Identifier' and isValid):
        return 'Identifier'
    elif (state == 'Identifier' and not isValid):
        return 'IdentifierFinal'
    return state + 'Error:_' + input;

def DelimiterAutomata(state: str, input: str):
    if (state == 'DelimiterFinal'):
        return 'DelimiterFinal';
    if (state == 'Delimiter'):
        return 'DelimiterFinal';
    return state + 'Error:_' + input;

def ErrorAutomata(state: str, input: str):
    return state + 'Error:_' + input;

def StringAutomata(state: str, input: str):
    if (state == 'String' and input == '"'):
        return 'StringFinal';
    if (state == 'String' and input == '\n'):
        return 'MalformedString';
    return 'String';

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
        return 'BlockCommentFinal'
    if (state == 'ClosingBlockComment' and not input == '/'):
        return 'BlockComment'
    if (state == 'BlockComment'):
        return 'BlockComment'
    return state + 'Error:_' + input;

def getNextState(state: str, input: str) -> str:
    if (not state == 'InitialState'):
        automata: Automata = findApropriateAutomata(state);
        return automata(state, input);
    if (input == '/'):
        return 'PossibleComment';
    elif (isDelimiter(input)):
        return 'Delimiter'
    elif (re.match( r'[a-zA-Z]+', input)):      # Se for uma letra
        return 'Identifier'
    elif (input == '"'):
        return 'String';
    return '0';

def isFinalState(state: str):
    finalStates = {
        'DelimiterFinal',
        'MalformedString',
        'StringFinal',
        'LineCommentFinal',
        'BlockCommentFinal',
        'ArithmeticFinal',
    };
    if state in finalStates:
        return True;
    return False;

def getTokenType(state: str):
    stateToTokenType = {
        'DelimiterFinal': 'DEL',
        'MalformedString': 'CMF',
        'StringFinal': 'CAC',
        'LineCommentFinal': 'COM',
        'BlockCommentFinal': 'CMB',
        'ArithmeticFinal': 'ART'
    }
    return stateToTokenType.get(state, 'None');

def toFinalState(state: str):
    return state + 'Final';

def findApropriateAutomata(state: str) -> Automata:
    if ('Identifier' in state):
        return IdendifierAutomata;
    elif ('Delimiter' in state):
        return DelimiterAutomata;
    elif ('String' in state):
        return StringAutomata;
    elif ('Comment' in state):
        return CommentAutomata;
    return ErrorAutomata;

def generateToken(state: str, lineNumber: int, lineText: str, tokenStartIndex: int, tokenEndIndex: int):
    tokenType = getTokenType(state);
    tokenText = lineText[tokenStartIndex:tokenEndIndex];
    if (tokenType == 'IDE'):
        tokenType = 'PRE' if isReserved(tokenText) else 'IDE';
    if (tokenType == 'CAC'):
        tokenType = 'CMF' if hasNonASCII(tokenText) else 'CAC';
    return Token(tokenType, lineNumber, tokenStartIndex, tokenEndIndex, tokenText);


def findTokensInString(line: str, lineCount: int, initialState: str, overflow: str) -> ResTokenList:
  lineLength: int = len(line);
  tokenStartIndex: int = 0;
  currentIndex: int = 0;
  currentState: str = initialState;
  tokensFoundInThisLine: list[Token] = [];
  tokenOverflow: str = overflow if initialState == '8' else '';

  exitLoop = False;

  while (not exitLoop and currentIndex < lineLength):
    # Se ainda no estado inicial, considere o caractere atual como inicio do token
    if (currentState == 'InitialState'):
        tokenStartIndex = currentIndex;
    
    # Caractere atual
    character: str = line[currentIndex];

    # Proximo estado, dado o caractere lido
    nextState: str = getNextState(currentState, character);

    # Se for um estado final, gere um token
    if (isFinalState(nextState)):
        token = generateToken(currentState, lineCount, line, tokenStartIndex, currentIndex);
        tokensFoundInThisLine.append(token);    # Apos salvar o token
        currentState = 'InitialState';          # Volte para o estado inicial
    
    # Do contrario, leia o proximo caractere
    else:
        # Se a linha termina e o estado não é final, decrementa o index
        # para chegar num estado final na proxima iteração
        if (currentIndex + 1 >= lineLength):
            nextState = toFinalState(nextState);    # Define o estado como final
            currentIndex = currentIndex - 1;

        # Se há um comentario de bloco multilinha
        if (currentState == 'BlockCommentOverflow'):
            tokenOverflow = line[tokenStartIndex:].replace('\n', '');
            exitLoop = True;

        currentState = nextState            # Define o priximo estado
        currentIndex = currentIndex + 1;

    if (currentState == '0'):
        if (line[currentIndex] == '&'):
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