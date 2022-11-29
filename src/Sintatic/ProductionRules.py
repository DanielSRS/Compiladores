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

# Expressao Aritmetica
Expressao = [['<ExpressaoMulti>', '<ExpressaoComMult>']];
ExpressaoComMult = [['<SimboloSomaSub>','<Expressao>'], []];
ExpressaoMulti =[['<Valor>', '<ExpressaoMultiComValor>']];
ExpressaoMultiComValor = [['*', '<ExpressaoMulti>'], ['/', '<ExpressaoMulti>'], []]
Valor = [['<Operavel>'],['(', '<Expressao>', ')']];

# Expressaõ relacional
ExpressaoRelacional = [['<ValorRelacional>', '<REL>', '<ValorRelacional>'], []]
ValorRelacional = [['-IDE', '<ValorRelacionalComIDE>'], ['-NRO'], ['-CAC'], ['(', '<ValorRelacionalComParentesis>'], ['<Boolean>']];
ValorRelacionalComIDE = [['(', '<ParametrosOpcionais>', ')'], ['.', '-IDE'], ['<DimensoesDeAcesso>'], []];
ValorRelacionalComParentesis = [['<ExpressaoRelacional>', ')'], ['<Expressao>', ')'], ['<ExpressaoLogica>', ')']];

# Expressão logica
ExpressaoLogica = [['<neg>', '<OperadorLogico>', '<Expressao Opcional>']];
ExpressaoOpcional = [['<op>', '<neg>', '<Expressao Opcional>'], []];
op = [['&&', '||']];
neg = [['<Negacao>'], ['<ValorRelacional>']];
OperadorLogico = [['&&', '<neg>'], ['||', '<neg>']];
Negacao = [['!', '<ValorRelacional>']];

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

# Chamada funcção
RetornoFuncao = [['-IDE', '(', '<ParametrosOpcionais>', ')']]
ParametrosOpcionais = [['<ListaDeParametros>'], []];
ListaDeParametros = [['<Parametro>', '<MultiplosParametros>']];
MultiplosParametros = [[',', '<ListaDeParametros>'], []];
Parametro = [['-IDE', '<ParametroComIDE>'], ['-NRO'], ['-CAC']];
ParametroComIDE = [['<DimensoesDeAcesso>'], ['.', '-IDE'], ['(', '<ParametrosOpcionais>', ')'], []];

# Chamada de função ou procedimento
ChamadaFuncao = [['<RetornoFuncao>', ';']];

# Bloco
Bloco = [['{,' '<Conteudos>', '}']]
Conteudos = [['<ConteudoDeBloco>', '<Conteudos>'], []]
ConteudoDeBloco = [['<Expressao>', ';'], ['<ExpressaoRelacional>', ';'], ['<ExpressaoLogica>', ';'], ['<Matriz>', ';'], ['<Print>'], ['<Read>'], ['<ChamadaFuncao>'], ['<If>'], ['<VarDeclaracao>'], ['<While>']]

# While Verificar expressao
While = [['while', '(', '<Exp>', ')', '<Bloco>' ]]  
Exp = [['<ExpressaoLogica>'], ['<Boolean>'], ['<ExpressaoRelacional>']]

# If
If = [['if', '(', '<Exp>', ')', 'then', '<ConteudoDoIf>']]
ConteudoDoIf = [['<Bloco>'], ['<Bloco>', 'else', '<Bloco>']]

# Declaração de função   ps: lista de parmeteros ta errada  
Funcao = [['function', '<Tipo>', '-IDE', '(', '<ListParametros>', ')', '<functionReturn>']]
functionReturn = [['{', '<Conteudos>', 'return', '<ValorRelacional>', ';' '}']]
ListParametros = [['<Parametro>'], ['<Parametro>', ',', '<ListParametros>'], []]
Parametro = [['<Tipo>', '-IDE']]
                 
# Tipo
Tipo = [['int'], ['real'], ['boolean'], ['string'], ['-IDE']]

# Procedimento
Procedimento = [['procedure', '-IDE', '(', '<ListParametros>', ')', '<Bloco>']]

# Variaveis globais
VarDeclaracao = [['var', '{', '<todasAsVars>', '}']]
Constantes = [['const', '{', '<todasAsVars>', '}']]
todasAsVars = [['<dvar>', '<todasAsVars>'], ['<dvar>']]

# Declaração de tipo composto
DeclaracaoStruct = [['struct', '-IDE', '{', '<todasAsVars>', '}']]

# Declaração de variavel
dvar = [['<Tipo>', '<varList>', ';']]
varList = [['-IDE', '<attopt>', ',', '<varList>'], ['-IDE', '<attopt>']]
attopt = [['=', '<ValorRelacional>'], []]

          
# Extends
Extendstc = [['-IDE', 'extends', '-IDE', '{', '<todasAsVars>', '}']]
         
Estrutura = [['<compOpt>', '<extOpt>', '<varOpt>', '<constOpt>', '<funcoes>']]
varOpt = [['<VarDeclaracao>'], []]
constOpt = [['<Constantes>'], []]
compOpt = [['<DeclaracaoStruct>', '<compOpt>'], []]
extOpt = [['<Extendstc>', '<extOpt>'], []]
funcoes = [['<funOuProc>', '<funcoes>'], ['<funOuProc>']]
funOuProc = [['<Funcao>'], ['<Procedimento>']]
           
Inicio = [['<Estrutura>']]
         

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
  '<RetornoFuncao>': RetornoFuncao,
  '<ParametrosOpcionais>': ParametrosOpcionais,
  '<ListaDeParametros>': ListaDeParametros,
  '<Parametro>': Parametro,
  '<ParametroComIDE>': ParametroComIDE,
  '<MultiplosParametros>': MultiplosParametros,
  '<ChamadaFuncao>': ChamadaFuncao,
  '<Expressao>': Expressao,
  '<ExpressaoMulti>': ExpressaoMulti,
  '<Valor>': Valor,
  '<ExpressaoMultiComValor>': ExpressaoMultiComValor,
  '<ExpressaoComMult>': ExpressaoComMult,
  '<ExpressaoRelacional>': ExpressaoRelacional,
  '<ValorRelacional>': ValorRelacional,
  '<ExpressaoLogica>': ExpressaoLogica,
  '<Expressao Opcional>': ExpressaoOpcional,
  '<op>': op,
  '<neg>': neg,
  '<OperadorLogico>': OperadorLogico,
  '<Negacao>': Negacao,
  '<ValorRelacionalComIDE>': ValorRelacionalComIDE,
  '<ValorRelacionalComParentesis>': ValorRelacionalComParentesis,

  '<Bloco>': Bloco,
  '<Conteudos>': Conteudos,
  '<ConteudoDeBloco>': ConteudoDeBloco,
  '<While>': While,
  '<Exp>': Exp,
  '<If>': If,
  '<ConteudoDoIf>': ConteudoDoIf,
  '<Funcao>': Funcao,
  '<functionReturn>': functionReturn,
  '<ListParametros>': ListParametros,
  '<Parametro>': Parametro,
  '<Tipo>': Tipo,
  '<Procedimento>': Procedimento,
  '<VarDeclaracao>': VarDeclaracao,
  '<Constantes>': Constantes,
  '<todasAsVars>': todasAsVars,
  '<DeclaracaoStruct>': DeclaracaoStruct,
  '<dvar>': dvar,
  '<varList>': varList,
  '<attopt>': attopt,
  '<Extendstc>': Extendstc,
  '<Estrutura>': Estrutura,

  '<varOpt>': varOpt,
  '<constOpt>': constOpt,
  '<compOpt>': compOpt,
  '<extOpt>': extOpt,
  '<funcoes>': funcoes,
  '<funOuProc>': funOuProc,
  '<Inicio>': Inicio,
};
