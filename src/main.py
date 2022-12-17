from Prooduction import Production, SemanticState, printSymbolTable
from Sintatic.ProductionRules import EstruturaDoPrograma
from TokenUtils.Token import Token
from TokenUtils.orderTokens import isError, orderTokens
from automata.findTokensInStringAutomata import findTokensInStringAutomata
from filesystem import ResTokenList, TokenListPerFile, listDirFiles, readFileLines

def findTokensInString(line: str, lineNumber: int, initialState: str, overflow: str) -> ResTokenList:
    # Se a linha estiver vaxia não fax nada
    tokens = findTokensInStringAutomata(line, lineNumber, initialState, overflow);
    return tokens;

# Conta a quantidade de error léxicos presentes em uma lista de tokens
def errorCount(tk: 'list[Token]'):
    ec = 0
    for t in tk:
        if (isError(t.token)):
            ec = ec + 1;
    return ec;

defaultSintaticState: SemanticState = { 
    'fowardType': None,
    'declaringStruct': None,
    'isInsideAWhile': False,
    'validating': False,
    'simbolo': None,
    'declarandoStruct': None
}

defaultSemanticState: SemanticState = { 
    'fowardType': None,
    'declaringStruct': None,
    'isInsideAWhile': False,
    'validating': True,
    'simbolo': None,
    'declarandoStruct': None,
}

def lexico():
  source_directory = 'entrada';

  entry_files: list[str] = listDirFiles(source_directory);

  tokenListPerFile: TokenListPerFile = {}

# para cada arquivo fonte na pasta de entrada
  for filename in entry_files:
    filepath = source_directory + '/' + filename; # define o caminho para o arquivo
    source_file = open(filepath, 'r'); # abre o arquivo
    tokensFound: list[Token] = readFileLines(source_file, findTokensInString); # le os arquivos e recupera os tokens
    tokensFound.sort(key=orderTokens);

    errorsNum = errorCount(tokensFound);

    # salva as informaações em um arquivo
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
    if (errorsNum == 0):
      print("\n\n-------------- Sintatico -------------- \n\n");
      #tokensFound.append(Token('EOF', tokensFound[-1].line, 0, 0, 'EOF'));

      # Executa a primeira vez para fazer a analise sintatic e criar a tabela de simbolos
      Production(EstruturaDoPrograma, tokensFound, '<EstruturaDoPrograma>', defaultSintaticState, 0);

      # Executa uma segunda vez para fazer a analise semantica usando a tabela populada na execução anterior
      #Production(EstruturaDoPrograma, tokensFound, '<EstruturaDoPrograma>', defaultSemanticState, 0);
      printSymbolTable();
  return;

lexico();
