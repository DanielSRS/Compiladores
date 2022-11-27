from typing import Dict, List


Rule = List[str];
ProductionRules = List[Rule];

# Operadores relacionais
REL = [['!='], ['=='], ['<'], ['<='], ['>'], ['>='], ['=']];

# Valor booleano
Boolean = [['true'], ['false']];

# Soma ou subtração
SimboloSomaSub = [['+'], ['-']];

# Operavel
Operavel = [['-IDE'], ['-NRO']];

# Matriz
Matriz = [['-IDE', '<DimensoesDeAcesso>']];
DimensoesDeAcesso = [['<Access>', '<end>']];
Access = [['[', '<Indice>', ']']];
end = [['<Access>'], []];
Indice = [['-NRO'], ['-IDE']];

# Print
Print = [['print', '(', '<ConteudoDoPrint>', ')', ';']];
ConteudoDoPrint = [['-IDE', '<ConteudoDoPrintComIDE>'], ['-CAC']];
ConteudoDoPrintComIDE = [['<DimensoesDeAcesso>'], ['.', '-IDE'], []];

# Tipo composto
comp = [['-IDE', '.', '-IDE']];

# Read
Read = [['read', '(', '<Ler>', ')', ';']];
Ler = [['-IDE', '<LerComIDE>']];
LerComIDE = [['<DimensoesDeAcesso>'], ['.', '-IDE'], []];

Mapped = Dict[str, ProductionRules]

map: Mapped = {
  '<Comp>': comp,
  '<Matriz>': Matriz,
  '<DimensoesDeAcesso>' : DimensoesDeAcesso,
  '<Access>': Access,
  '<end>': end,
  '<Indice>': Indice,
  '<REL>': REL,
  '<Boolean>': Boolean,
  '<SimboloSomaSub>': SimboloSomaSub,
  '<Operavel>': Operavel,
  '<Print>': Print,
  '<ConteudoDoPrint>': ConteudoDoPrint,
  '<ConteudoDoPrintComIDE>': ConteudoDoPrintComIDE,
  '<Read>': Read,
  '<Ler>': Ler,
  '<LerComIDE>': LerComIDE,
};
