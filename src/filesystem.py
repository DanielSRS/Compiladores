from io import TextIOWrapper
from os import listdir
from os.path import isfile, join
from typing import Callable, NamedTuple, TypeVar

T = TypeVar('T');

class Token(NamedTuple):
  token: str;
  line: int;
  tokenStartIndex: int;
  tokenEndIndex: int;
  value: str;

class ResTokenList(NamedTuple):
  lastState: int;
  lastStartTokenIndex: int;
  tokenStartLine: int;
  tokenOverflow: str;
  tokenList: 'list[Token]';


"""
  Lista todos os arquivos de um dado diretorio

  Retorna um lista de strings com os nomes dos arqivos
"""
def listDirFiles(dirPath: str) -> 'list[str]': 
  onlyfiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
  return onlyfiles;

def readFileLines(opened_file: TextIOWrapper, on_line: Callable[[str, int, int, str], ResTokenList]):
  # Lê cada linha do arquivo e passa para a função de callback on_line

  response: list[Token] = [];
  currentState: ResTokenList = ResTokenList(0, 0, 0, '', []);

  # Loop through each line via file handler
  for count, line in enumerate(opened_file):
    if (line == ''):
      print('Fim do arquivo')
    res = on_line(line, count + 1, currentState.lastState, currentState.tokenOverflow);
    response = response + res.tokenList;
    currentState = res;
  
  if (currentState.lastState == 8):
    t = Token('Bloco mal', currentState.tokenStartLine, currentState.lastStartTokenIndex, 0, currentState.tokenOverflow);
    response.append(t);
  
  return response;

