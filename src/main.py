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
    isValid = re.match(r'[a-zA-Z]+', input) or re.match(r'\d', input) or input == '_';
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
        return 'StringComplete';
    if (state == 'StringComplete'):
        return 'StringFinal';
    if (state == 'String' and input == '\n'):
        return 'MalformedString';
    if (state == 'MalformedString' and input == '\n'):
        return 'MalformedStringFinal';
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
        return 'BlockCommentComplete'
    if (state == 'BlockCommentComplete'):
        return 'BlockCommentFinal'
    if (state == 'ClosingBlockComment' and not input == '/'):
        return 'BlockComment'
    if (state == 'BlockComment'):
        return 'BlockComment'
    return state + 'Error:_' + input;

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

def RelationalOperatorAutomata(state: str, input: str):
    if (state == 'Relational' and input == '='):
        return 'DoubleRelationalOperator'
    if (state == 'DoubleRelationalOperator'):
        return 'RelationalOperatorFinal'
    return 'RelationalOperatorFinal';

def ArithmeticOperatorAutomata(state: str, input: str):
    if (state == 'Arithmetic' and input == '+'):
        return 'DoubleArithmeticOperator'
    if (state == 'DoubleArithmeticOperator'):
        return 'ArithmeticOperatorFinal'
    if (state == 'Arithmetic*'):
        return 'ArithmeticOperatorFinal'
    if (state == 'Arithmetic-' and input == '-'):
        return 'DoubleArithmeticOperator'
    if (state == 'DoubleArithmeticOperator'):
        return 'ArithmeticOperatorFinal'
    if (state == 'Arithmetic-' and input == ' '):
        return 'ArithmeticPossibleNROorART'
    if (state == 'Arithmetic-' and re.match(r'\d', input)):
        return 'Number'
    if (state == 'ArithmeticPossibleNROorART' and re.match(r'\d', input)):
        return 'Number'
    if (state == 'ArithmeticPossibleNROorART' and input == ' '):
        return 'ArithmeticPossibleNROorART'
    if (state == 'ArithmeticPossibleNROorART'):
        return 'ArithmeticOperatorFinal'
    if (state == 'PossibleArithmeticMinus' and input == ' ' or input == '\t'):
        return 'PossibleArithmeticMinus'
    if (state == 'PossibleArithmeticMinus' and re.match(r'\d', input)):
        return 'ArithmeticOperatorFinal'
    if (state == 'PossibleArithmeticMinus'):
        return 'GoBack'
    return 'ArithmeticOperatorFinal';

def NumbertAutomata(state: str, input: str):
    if (state == 'Number' and re.match(r'\d', input)):
        return 'Number'
    if (state == 'Number' and input == '.'):
        return 'FPNumber'
    if (state == 'FPNumber' and re.match(r'\d', input)):
        return 'FPNumberComplete'
    if (state == 'FPNumberComplete' and re.match(r'\d', input)):
        return 'FPNumberComplete'
    if (state == 'FPNumberComplete' and not re.match(r'\d', input)):
        return 'NumberFinal'
    if (state == 'FPNumber' and not re.match(r'\d', input)):
        return 'MalformedNumberFinal'
    if (state == 'Number' and not (input == ' ' or input == '-' or input == '\t')):
        return 'NumberFinal'
    if (state == 'Number' and (input == ' ' or input == '-' or input == '\t')):
        return 'NumberFinalInPossibleOperation'
    if (state == 'NumberFinalInPossibleOperation' and (input == ' ' or input == '\t')):
        return 'NumberFinalInPossibleOperation_'
    if (state == 'NumberFinalInPossibleOperation_' and (input == ' ' or input == '\t')):
        return 'NumberFinalInPossibleOperation_'
    if (state == 'NumberFinalInPossibleOperation' and input == '-'):
        return 'PossibleArithmeticMinus'
    if (state == 'NumberFinalInPossibleOperation_' and input == '-'):
        return 'PossibleArithmeticMinus'
    if (state == 'NumberFinalInPossibleOperation'):
        return 'InitialState'
    if (state == 'NumberFinalInPossibleOperation_'):
        return 'InitialState'
    else:  # esse else ta errado
        return 'NumberFinal'

def getNextState(state: str, input: str) -> str:
    if (state == 'MalformedToken'):
        return 'MalformedTokenFinal';
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
    elif (input == '&'):
        return 'PossibleLogical&&';
    elif (input == '|'):
        return 'PossibleLogical||';
    elif (input == '!'):
        return 'PossibleLogical!';
    elif (input == '=' or input == '<' or input == '>'):
        return 'Relational';
    elif (input == '+'):
        return 'Arithmetic';
    elif (input == '*'):
        return 'Arithmetic*';
    elif (input == '-'):
        return 'Arithmetic-';
    elif (re.match(r'\d', input)):
        return 'Number';
    elif (input == ' ' or input == '\t' or input == '\n'):
        return ('InitialState');
    return 'MalformedToken';

def isFinalState(state: str):
    finalStates = {
        'DelimiterFinal',
        'MalformedStringFinal',
        'StringFinal',
        'LineCommentFinal',
        'BlockCommentFinal',
        'ArithmeticFinal',
        'LogicalOperatorFinal',
        'NumberFinal',
        'ArithmeticOperatorFinal',
        'RelationalOperatorFinal',
        'IdentifierFinal',
        'MalformedNumberFinal',
        'MalformedTokenFinal',
    };
    if state in finalStates:
        return True;
    return False;

def getTokenType(state: str):
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
    elif ('Logical' in state):
        return LogicalOperatorAutomata;
    elif ('Relational' in state):
        return RelationalOperatorAutomata;
    elif ('Arithmetic' in state):
        return ArithmeticOperatorAutomata;
    elif ('Number' in state):
        return NumbertAutomata;
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
  tokenOverflow: str = overflow if initialState == 'BlockComment' else '';

  exitLoop = False;

  while (not exitLoop and currentIndex < lineLength):
    # Se ainda no estado inicial, considere o caractere atual como inicio do token
    if (currentState == 'InitialState'):
        tokenStartIndex = currentIndex;
    
    # Caractere atual
    character: str = line[currentIndex];

    # Proximo estado, dado o caractere lido
    nextState: str = getNextState(currentState, character);

    if (nextState == 'NumberFinalInPossibleOperation'):
        token = generateToken('NumberFinal', lineCount, line, tokenStartIndex, currentIndex);
        tokensFoundInThisLine.append(token);
        tokenStartIndex = currentIndex;
        currentIndex = currentIndex - 1;
    
    if (nextState == 'GoBack'):
        nextState = 'InitialState'; 
        currentIndex = tokenStartIndex - 1;

    # Se for um estado final, gere um token
    if (isFinalState(nextState)):
        token = generateToken(nextState, lineCount, line, tokenStartIndex, currentIndex);
        if (not (token.token == 'COM' or token.token == 'CMB')):
            tokensFoundInThisLine.append(token);    # Apos salvar o token
        currentState = 'InitialState';          # Volte para o estado inicial
    
    # Do contrario, leia o proximo caractere
    else:
        # Se a linha termina e o estado não é final, decrementa o index
        # para chegar num estado final na proxima iteração
        if (currentIndex + 1 >= lineLength and not (nextState == 'InitialState' or nextState == 'BlockCommentOverflow')):
            nextState = getNextState(nextState, '\n');
            currentIndex = currentIndex + 2;
            token = generateToken(nextState, lineCount, line, tokenStartIndex, currentIndex);
            if (not (token.token == 'COM' or token.token == 'CMB' or token.token == 'None')):
                tokensFoundInThisLine.append(token);    # Apos salvar o token
            currentState = 'InitialState';

        currentState = nextState            # Define o priximo estado
        currentIndex = currentIndex + 1;

  if (currentState != 'BlockCommentOverflow'):
    currentState = 'InitialState';
  else:
    tokenOverflow = tokenOverflow + line[tokenStartIndex:].replace('\n', '');
    currentState = 'BlockComment';
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