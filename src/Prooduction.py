from typing import Dict

from TokenUtils.Token import Token


comp = ['IDE', '.', 'IDE'];

Mapped = Dict[str, 'list[str]']

map: Mapped = {
  '<Comp>': comp,
};

t_comp = [Token('IDE', 1, 0, 2, 'val'), Token('DEL', 1, 0, 2, '.'), Token('IDE', 1, 0, 2, 'val')]


def isNonTerminal(token: str):
  if (token[0] == '<'):
    return True;
  return False;


def Production(prod: 'list[str]', tokens: 'list[Token]'):
  errors: list[str] = [];
  for to in prod:
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