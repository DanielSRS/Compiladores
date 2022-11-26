from typing import Dict, List, Optional, TypedDict

from TokenUtils.Token import Token

Rule = List[str];
ProductionRules = List[Rule];


comp = [['-IDE', '.', '-IDE']];

#Matriz
Matriz = [['-IDE', '<DimensoesDeAcesso>']];
DimensoesDeAcesso = [['<Access>', '<end>']];
Access = [['[', '<Indice>', ']']];
end = [['<Access>'], []];
Indice = [['-NRO'], ['-IDE']];

Mapped = Dict[str, ProductionRules]

map: Mapped = {
  '<Comp>': comp,
  '<Matriz>': Matriz,
  '<DimensoesDeAcesso>' : DimensoesDeAcesso,
  '<Access>': Access,
  '<end>': end,
  '<Indice>': Indice,
};

t_comp = [Token('IDE', 1, 0, 2, 'val'),
          Token('DEL', 1, 0, 2, '.'),
          Token('IDE', 1, 0, 2, 'val')]


def isNonTerminal(token: str):
  if (token[0] == '<'):
    return True;
  return False;

def isSemiTerminal(sm: str):
  semis = { '-IDE', };
  if sm in semis:
    return True;
  return False;

def matchSemiterminal(received: str, target: str):
  sanitazed = target[1:];
  return True if received == sanitazed else False;

# Dado as regras de uma produção, retorna
# o conjunto fisrt dessa produção.
#
# O conjuto first é uma lista de listas de string,
# onde cada lista de string representa o conjunto fisrt 
# uma das regras da produção. dado que 
# Cada produção é formada por uma ou mais regras
def getFists(productionRules: ProductionRules):
  #para cada regra da produção, retorna uma lista de strings
  conjuntoFisrt: List[List[str]] = [];
  for rule in productionRules:
    if (len(rule) == 0):                              # Se for uma produção vazia
      conjuntoFisrt.append([""]);                     # coloca uma string varia no conjunto first
    elif (isNonTerminal(rule[0])):                    # se o primerio elemento for um não terminal
      elemProduction = map.get(rule[0]);              # Busca a produção desse não terminal
      if (elemProduction == None):                    # Se a procução não existe
        raise Exception("Produção inexistente");      # Há um erro
      l: List[str] = [];
      for lst in getFists(elemProduction):            # Encontra o conjunto fist da produção
        l.extend(lst);                                # Transforma em uma unica lista de string
      conjuntoFisrt.append(l);                        # Adiciona lista ao conjuto da prudção atual
    else:                                             # Se form um terminal
      conjuntoFisrt.append([rule[0]]);
  return conjuntoFisrt;                               # Retorna o conjunto encontrado

def chooseProduction(production: ProductionRules, token: Token) -> Optional[int]:
  conjuntoFist = getFists(production);
  for index, listOffists in enumerate(conjuntoFist):
    if token.value in listOffists:
      return index;
    if "-" + token.token in listOffists:
      return index;

class ProductionRes(TypedDict):
  tokenIndex: int

def Production(prod: ProductionRules, tokens: 'list[Token]', initialTokenindex: int = 0) -> ProductionRes:
  errors: list[str] = [];                                                     # Lista de erros entontrados
  tokenIndex = initialTokenindex;                                             # Index do token lido
  if (len(tokens) < 1):                                                       # Se não houver mais tokens
    raise Exception("Não há tokens suficientes");

  lookahead: Token = tokens[tokenIndex];                                      # toke sendo verificado
  productionIndex = chooseProduction(prod, lookahead);                        # Escolhe a regra adequada, de acordo com  a 
                                                                              # produção tual
  
  if (productionIndex == None):                                               # Se o token atula não fizer parte das regras da produção
    raise Exception('Não encotrada produção adequada');
  
  rule: Rule = prod[productionIndex];                                         # Define a regra de produção a ser usada
  print("selected rule index: ", productionIndex, "\n");
  print(rule);

  for to in rule:
    if (tokenIndex >= len(tokens)):
      errmsg = "Esperado: " + to + " mas encotrado fim de arquivo (EOF)";
      raise Exception(errmsg);
    lookahead = tokens[tokenIndex];
    if (isNonTerminal(to)):                                                  # Se for um não terminal
      p = map.get(to);                                                       # Encontra a produção para esse não terminal
      if (p == None):                                                        # Erro caso  a produção não exista
        raise Exception("Produção inexistente!!");
      res = Production(p, tokens, tokenIndex);
      tokenIndex = res['tokenIndex'] - 1;
    
    elif (isSemiTerminal(to)):                                               # Se for um terminal, cujo valor do token não é importante
      if (matchSemiterminal(lookahead.token, to)):                           # verifica o apenas se o tipo do token é o esperado
        print("Passado ", to);
      else:
        msg = "Esperado: " + to + " mas recebido" + lookahead.token;
        raise Exception(msg);
    elif (to == lookahead.value):                                            # se for um termina, verifica se o valor recebido é igual
      print("Passado del");                                                  # ao valor esperao
    else:                                                                    # se não for, lança erro
      raise Exception('Esperado ' + to + " mas recebido: " + lookahead.value);
    tokenIndex = tokenIndex + 1;
  return {
    'tokenIndex': tokenIndex,
  };

  
if __name__ == "__main__":
  Production(comp, t_comp);