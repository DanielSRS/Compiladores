from typing import Dict, List

from TokenUtils.Token import Token

Rule = List[str];
ProductionRules = List[Rule];


comp = [['IDE', '.', 'IDE']];

Mapped = Dict[str, ProductionRules]

map: Mapped = {
  '<Comp>': comp,
};

t_comp = [Token('IDE', 1, 0, 2, 'val'), Token('DEL', 1, 0, 2, '.'), Token('IDE', 1, 0, 2, 'val')]


def isNonTerminal(token: str):
  if (token[0] == '<'):
    return True;
  return False;

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


def Production(prod: ProductionRules, tokens: 'list[Token]'):
  errors: list[str] = [];
  rule = prod[0];
  for to in rule:
    lookahead = tokens.pop();
    if (isNonTerminal(to)):
      p = map.get(to);
      if (p == None):
        print("Produção inexistente!!");
        return;
      Production(p, tokens);
    if (to == 'IDE'):
      if (lookahead.token == 'IDE'):
        print("Passado ide");
    elif (to == lookahead.value):
      print("Passado del");
    else:
      errors.append('teve erro');
  if (len(errors) == 0):
    print("Passed!");
  else:
    for e in errors:
      print(e);

  
if __name__ == "__main__":
  Production(comp, t_comp);