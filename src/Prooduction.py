from typing import List, Optional, TypedDict
from TokenUtils.Token import Token
from Sintatic.ProductionRules import map, ProductionRules, Rule, REL, Boolean, SimboloSomaSub, Operavel, Matriz, Print, comp, Read, RetornoFuncao, ChamadaFuncao, Expressao


# Testes relacionais
t_rel_diff = [Token('REL', 1, 0, 2, '!=')];
t_rel_eq = [Token('REL', 1, 0, 2, '==')];
t_rel_lt = [Token('REL', 1, 0, 2, '<')];
t_rel_leq = [Token('REL', 1, 0, 2, '<=')];
t_rel_gt = [Token('REL', 1, 0, 2, '>')];
t_rel_geq = [Token('REL', 1, 0, 2, '>=')];
t_rel_atr = [Token('REL', 1, 0, 2, '=')];

# Testes booleanos
t_bool_true = [Token('PRE', 1, 0, 2, 'true')];
t_bool_false = [Token('PRE', 1, 0, 2, 'false')];

# Testes operadores de soma e subtração
t_somasub_soma = [Token('ART', 1, 0, 2, '+')];
t_somasub_sub = [Token('ART', 1, 0, 2, '-')];

# Testes operavel
t_operavel_IDE = [Token('IDE', 1, 0, 2, 'identificador')];
t_operavel_NRO = [Token('NRO', 1, 0, 2, '78554')];

# Testes matriz
t_matrix_single_nro = [
  Token('IDE', 1, 0, 2, 'mat'),
  Token('DEL', 1, 0, 2, '['),
  Token('NRO', 1, 0, 2, '61'),
  Token('DEL', 1, 0, 2, ']'),
]
t_matrix_single_IDE = [
  Token('IDE', 1, 0, 2, 'mat'),
  Token('DEL', 1, 0, 2, '['),
  Token('IDE', 1, 0, 2, 'identificador'),
  Token('DEL', 1, 0, 2, ']'),
]
t_matrix_multiplo = [
  Token('IDE', 1, 0, 2, 'mat'),
  Token('DEL', 1, 0, 2, '['),
  Token('IDE', 1, 0, 2, 'identificador'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, '['),
  Token('NRO', 1, 0, 2, '61'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, '['),
  Token('NRO', 1, 0, 2, '61'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, '['),
  Token('IDE', 1, 0, 2, 'identificador'),
  Token('DEL', 1, 0, 2, ']'),
]

# Print
t_print_IDE = [
  Token('IDE', 1, 0, 2, 'print'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'identificador'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]
t_print_CAC = [
  Token('IDE', 1, 0, 2, 'print'),
  Token('DEL', 1, 0, 2, '('),
  Token('CAC', 1, 0, 2, '"String"'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]
t_print_Matriz = [
  Token('IDE', 1, 0, 2, 'print'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'matrix'),
  Token('DEL', 1, 0, 2, '['),
  Token('NRO', 1, 0, 2, '9'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, '['),
  Token('IDE', 1, 0, 2, 'index'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]
t_print_Comp = [
  Token('IDE', 1, 0, 2, 'print'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'tipoComposto'),
  Token('DEL', 1, 0, 2, '.'),
  Token('IDE', 1, 0, 2, 'propriedade'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]

# Tipo composto
t_comp = [
  Token('IDE', 1, 0, 2, 'TipoComposto'),
  Token('DEL', 1, 0, 2, '.'),
  Token('IDE', 1, 0, 2, 'atributo'),
  Token('DEL', 1, 0, 2, ';'),
]

# Teste read
t_readt_IDE = [
  Token('IDE', 1, 0, 2, 'read'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'identificador'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]
t_read_Matriz = [
  Token('IDE', 1, 0, 2, 'read'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'matrix'),
  Token('DEL', 1, 0, 2, '['),
  Token('IDE', 1, 0, 2, 'index'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]
t_read_Comp = [
  Token('IDE', 1, 0, 2, 'read'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'tipoComposto'),
  Token('DEL', 1, 0, 2, '.'),
  Token('IDE', 1, 0, 2, 'propriedade'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]

# Retorno função
t_retunFunction_empty = [
  Token('IDE', 1, 0, 2, 'fun'),
  Token('DEL', 1, 0, 2, '('),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_1IDE = [
  Token('IDE', 1, 0, 2, 'fun2'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'param1'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_2IDE = [
  Token('IDE', 1, 0, 2, 'fun5'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'param1'),
  Token('DEL', 1, 0, 2, ','),
  Token('IDE', 1, 0, 2, 'param2'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_NRO = [
  Token('IDE', 1, 0, 2, 'fun3'),
  Token('DEL', 1, 0, 2, '('),
  Token('NRO', 1, 0, 2, '45'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_CAC = [
  Token('IDE', 1, 0, 2, 'fun4'),
  Token('DEL', 1, 0, 2, '('),
  Token('CAC', 1, 0, 2, '"string  jksjlf"'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_Matriz = [
  Token('IDE', 1, 0, 2, 'fun6'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'acessoMatrix'),
  Token('DEL', 1, 0, 2, '['),
  Token('NRO', 1, 0, 2, '132'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_comp = [
  Token('IDE', 1, 0, 2, 'fun7'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'struct'),
  Token('DEL', 1, 0, 2, '.'),
  Token('IDE', 1, 0, 2, 'prop'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_retunFunction1 = [
  Token('IDE', 1, 0, 2, 'fun8'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'myFunctionCall'),
  Token('DEL', 1, 0, 2, '('),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_retunFunction2 = [
  Token('IDE', 1, 0, 2, 'fun9'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'read'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'matrix'),
  Token('DEL', 1, 0, 2, '['),
  Token('IDE', 1, 0, 2, 'index'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ')'),
]
t_retunFunction_multiple = [
  Token('IDE', 1, 0, 2, 'fun9'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'read'),
  Token('DEL', 1, 0, 2, '('),
  Token('IDE', 1, 0, 2, 'matrix'),
  Token('DEL', 1, 0, 2, '['),
  Token('IDE', 1, 0, 2, 'index'),
  Token('DEL', 1, 0, 2, ']'),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ','),
  Token('IDE', 1, 0, 2, 'param2'),
  Token('DEL', 1, 0, 2, ','),
  Token('CAC', 1, 0, 2, '"string  jksjlf"'),
  Token('DEL', 1, 0, 2, ','),
  Token('NRO', 1, 0, 2, '132'),
  Token('DEL', 1, 0, 2, ','),
  Token('NRO', 1, 0, 2, '132'),
  Token('DEL', 1, 0, 2, ')'),
]

# Cahamada função ou procedimento
t_chamada = [
  Token('IDE', 1, 0, 2, 'function_ou_procedure'),
  Token('DEL', 1, 0, 2, '('),
  Token('DEL', 1, 0, 2, ')'),
  Token('DEL', 1, 0, 2, ';'),
]

# Expressão aritimetica
t_aritimetic_IDE_Plus_NRO = [
  Token('IDE', 1, 0, 2, 'aritimetic_value'),
  Token('ART', 1, 0, 2, '+'),
  Token('NRO', 1, 0, 2, '45'),
]
t_aritimetic_NRO_Plus_NRO = [
  Token('NRO', 1, 0, 2, '12'),
  Token('ART', 1, 0, 2, '+'),
  Token('NRO', 1, 0, 2, '98'),
]
t_aritimetic_IDE_Mult_IDE = [
  Token('NRO', 1, 0, 2, 'valor_ide'),
  Token('ART', 1, 0, 2, '*'),
  Token('NRO', 1, 0, 2, 'parcela'),
]
t_aritimetic_Mix = [
  Token('IDE', 1, 0, 2, 'valor_ide'),
  Token('ART', 1, 0, 2, '+'),
  Token('NRO', 1, 0, 2, '54'),
  Token('ART', 1, 0, 2, '/'),
  Token('NRO', 1, 0, 2, '65'),
  Token('ART', 1, 0, 2, '*'),
  Token('IDE', 1, 0, 2, 'idefa'),
  Token('ART', 1, 0, 2, '+'),
  Token('IDE', 1, 0, 2, 'lkej'),
  Token('ART', 1, 0, 2, '/'),
  Token('DEL', 1, 0, 2, '('),
  Token('NRO', 1, 0, 2, '3'),
  Token('ART', 1, 0, 2, '-'),
  Token('NRO', 1, 0, 2, '6'),
  Token('DEL', 1, 0, 2, ')'),
]


def isNonTerminal(token: str):
  if (token[0] == '<' and token[len(token) - 1] == '>'):
    return True;
  return False;

def isSemiTerminal(sm: str):
  semis = { '-IDE', '-NRO', '-CAC' };
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
  res = False;
  for rule in production:
    if (len(rule) < 1):
      res = True;
      continue;
    for r in rule:
      if (canRuleBeEmpty(r)):
        res = True;
  return res;

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
      print("Passado: ", to);                                                  # ao valor esperao
    else:                                                                    # se não for, lança erro
      raise Exception('Esperado ' + to + " mas recebido: " + lookahead.value);
    tokenIndex = tokenIndex + 1;
  return {
    'tokenIndex': tokenIndex,
  };

  
if __name__ == "__main__":
  # Testes de operador relacional
  print("------ Relacionais ------");
  Production(REL, t_rel_eq);
  Production(REL, t_rel_diff);
  Production(REL, t_rel_geq);
  Production(REL, t_rel_gt);
  Production(REL, t_rel_leq);
  Production(REL, t_rel_lt);
  Production(REL, t_rel_atr);

  # Testes booleanos
  print("------ Booleanos ------");
  Production(Boolean, t_bool_true);
  Production(Boolean, t_bool_false);

  # Testes operadores de soma e subtração
  print("------ SomaSub ------");
  Production(SimboloSomaSub, t_somasub_soma);
  Production(SimboloSomaSub, t_somasub_sub);

  # Testes operadores de soma e subtração
  print("------ Operavel ------");
  Production(Operavel, t_operavel_IDE);
  Production(Operavel, t_operavel_NRO);

  # Testes matriz
  print("------ Matriz ------");
  Production(Matriz, t_matrix_single_IDE);
  Production(Matriz, t_matrix_single_nro);
  Production(Matriz, t_matrix_multiplo);

  # Testes matriz
  print("------ Print ------");
  Production(Print, t_print_CAC);
  Production(Print, t_print_IDE);
  Production(Print, t_print_Comp);
  Production(Print, t_print_Matriz);

  # Testes matriz
  print("------ Tipo composto ------");
  Production(comp, t_comp);

  # Testes read
  print("------ Print ------");
  Production(Read, t_read_Comp);
  Production(Read, t_read_Matriz);
  Production(Read, t_readt_IDE);

  # Testes retorno de função
  print("------ RetornoFuncao ------");
  Production(RetornoFuncao, t_retunFunction_empty);
  Production(RetornoFuncao, t_retunFunction_1IDE);
  Production(RetornoFuncao, t_retunFunction_2IDE);
  Production(RetornoFuncao, t_retunFunction_NRO);
  Production(RetornoFuncao, t_retunFunction_CAC);
  Production(RetornoFuncao, t_retunFunction_Matriz);
  Production(RetornoFuncao, t_retunFunction_comp);
  Production(RetornoFuncao, t_retunFunction_retunFunction1);
  Production(RetornoFuncao, t_retunFunction_retunFunction2);

  # Testes de chamada de função ou procedimento
  print("------ ChamadaFuncao ------");
  Production(ChamadaFuncao, t_chamada);

  # Testes de operaçãoes aritimeticas
  print("------ Expressao ------");
  Production(Expressao, t_aritimetic_IDE_Plus_NRO);
  Production(Expressao, t_aritimetic_NRO_Plus_NRO);
  Production(Expressao, t_aritimetic_IDE_Mult_IDE);
  Production(Expressao, t_aritimetic_Mix);