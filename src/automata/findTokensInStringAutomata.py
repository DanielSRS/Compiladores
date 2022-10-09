import re
from TokenUtils.Token import Token
from TokenUtils.generateTokenFromState import generateTokenFromState
from automata.findApropriateAutomata import Automata, findApropriateAutomata
from filesystem import ResTokenList

def findTokensInStringAutomata(line: str, lineCount: int, initialState: str, overflow: str) -> ResTokenList:
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
        token = generateTokenFromState('NumberFinal', lineCount, line, tokenStartIndex, currentIndex);
        tokensFoundInThisLine.append(token);
        tokenStartIndex = currentIndex;
        currentIndex = currentIndex - 1;
    
    if (nextState == 'GoBack'):
        nextState = 'InitialState'; 
        currentIndex = tokenStartIndex - 1;

    # Se for um estado final, gere um token
    if (isFinalState(nextState)):
        token = generateTokenFromState(nextState, lineCount, line, tokenStartIndex, currentIndex);
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
            token = generateTokenFromState(nextState, lineCount, line, tokenStartIndex, currentIndex);
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

# verifica se um caractere é um delimitador
def isDelimiter(charactere: str) -> bool:
    delimiters = {'.', ';', ',', '(', ')', '[', ']', '{', '}'}
    if charactere in delimiters:
        return True
    return False

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

