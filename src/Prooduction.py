from typing import List, Optional, TypedDict
from TokenUtils.Token import Token
from Sintatic.ProductionRules import map, ProductionRules, Rule

def isNonTerminal(token: str):
  if (token[0] == '<' and token[len(token) - 1] == '>'):
    return True;
  return False;

def isSemiTerminal(sm: str):
  semis = { '-IDE', '-NRO', '-CAC', '-LOG', '-ART', '-PRE' };
  if sm in semis:
    return True;
  return False;

def canRuleBeEmpty(rule: str):
  if (isNonTerminal(rule)):
    production = map.get(rule);
    if (production == None):
      raise Exception("Não foi possivel verifica se é vazio!!");
    for conjunto in getFists(production):
      if "" in conjunto:
        return True;
  return False;

def canProductionBeEmpty(production: ProductionRules):
  for conjunto in getFists(production):
    if "" in conjunto:
      return True

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
      l: List[str] = [];
      nonEmpty = False;
      for tokentype in rule:
        if (nonEmpty):
          continue;
        elemProduction = map.get(tokentype);              # Busca a produção desse não terminal
        if (elemProduction == None):                    # Se a procução não existe
          raise Exception("Produção: ", tokentype, "inexistente");      # Há um erro
        for lst in getFists(elemProduction):            # Encontra o conjunto fist da produção
          l.extend(lst);                                # Transforma em uma unica lista de string
        if (not canRuleBeEmpty(tokentype)):
          nonEmpty = True;
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
  # errors: list[str] = [];                                                   # Lista de erros entontrados
  tokenIndex = initialTokenindex;                                             # Index do token lido
  if (len(tokens) < 1):                                                       # Se não houver mais tokens
    raise Exception("Não há tokens suficientes");

  lookahead: Token = tokens[tokenIndex];                                      # toke sendo verificado
  productionIndex = chooseProduction(prod, lookahead);                        # Escolhe a regra adequada, de acordo com  a 
                                                                              # produção tual
  
  if (productionIndex == None):                                               # Se o token atula não fizer parte das regras da produção
    if (canProductionBeEmpty(prod)):
      return {
        'tokenIndex': tokenIndex,
      }
    raise Exception('Não encotrada produção adequada');
  
  rule: Rule = prod[productionIndex];                                         # Define a regra de produção a ser usada
  print("selected rule index: ", productionIndex, "\n");
  print(rule);

  for to in rule:
    if (tokenIndex >= len(tokens)):
      if (canRuleBeEmpty(to)):                                                   # Se a produção pode ser vazia e não há mais tokens 
        tokenIndex = tokenIndex + 1;                                         # Icrement o token, pois a execução do loop vai ser interrompida
        continue;                                                            # Pula para a proxima iteração do loop
      errmsg = "Esperado: " + to + " mas encotrado fim de arquivo (EOF)";
      raise Exception(errmsg);
    lookahead = tokens[tokenIndex];
    if (isNonTerminal(to)):                                                  # Se for um não terminal
      p = map.get(to);                                                       # Encontra a produção para esse não terminal
      if (p == None):      
        print("\n\n-- produção tentado entcontrar");
        print(to);                                                  # Erro caso  a produção não exista
        raise Exception("Produção inexistente!!");
      res = Production(p, tokens, tokenIndex);
      tokenIndex = res['tokenIndex'] - 1;
    
    elif (isSemiTerminal(to)):                                               # Se for um terminal, cujo valor do token não é importante
      if (matchSemiterminal(lookahead.token, to)):                           # verifica o apenas se o tipo do token é o esperado
        print("Passado ", to, " - ", lookahead.value);
      else:
        msg = "Esperado: " + to + " mas recebido" + lookahead.token;
        raise Exception(msg);
    elif (to == lookahead.value):                                            # se for um termina, verifica se o valor recebido é igual
      print("Passado: ", to, " - ", lookahead.value);                                                  # ao valor esperao
    else:                                                                    # se não for, lança erro
      print(rule);
      print(lookahead);
      raise Exception('Esperado ' + to + " mas recebido: " + lookahead.value);
    tokenIndex = tokenIndex + 1;
  return {
    'tokenIndex': tokenIndex,
  };

  
if __name__ == "__main__":
  # Testes de operador relacional
  d = 54;