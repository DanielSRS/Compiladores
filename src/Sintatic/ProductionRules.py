from typing import Dict, List


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
