from typing import Dict, List


Rule = List[str];
ProductionRules = List[Rule];

# Operadores relacionais
REL = [['!='], ['=='], ['<'], ['<='], ['>'], ['>='], ['=']];

EstruturaDoPrograma = [[
  '<OpcionaisConstantes>',
  '<OpcionalStruct>',
  '<OpcionaislVariaveisGlobais>',
  '<AreaDeFuncoesEProcedimentos>'
]]

# Valor booleano          
Boolean = [['true'], ['false']]
 
   
# Definição da quantidade de Dimensoes de acesso a uma variavel de forma opcional
OpcionalDimensoesDeAcesso = [['<DimensoesDeAcesso>'], []]


# Definição da quantidade de Dimensoes de acesso de uma matriz
DimensoesDeAcesso = [['<TamanhoDaDimensao>', '<DimensaoOpcional>']];
TamanhoDaDimensao = [['[', '<IndiceDeAcesso>', ']']];
DimensaoOpcional = [['<TamanhoDaDimensao>', '<DimensaoOpcional>'], []]; 
IndiceDeAcesso = [['-NRO'], ['-IDE'], []];
           

# Declaração opcional de uma estrutura
OpcionalStruct = [['<DeclaracaoStruct>', '<OpcionalStruct>'], []]
                  

# Declaração de um tipo composto
DeclaracaoStruct = [['struct', '-IDE', '<CorpoDaEstrutura>']]
# Corpo de uma estrutura ou especialização de uma estrutura
CorpoDaEstrutura = [['{', '<VariaveisDaStruct>', '}'], ['<EspecializacaoDeStruct>']];               
# Extends de uma struct
EspecializacaoDeStruct = [['extends', '-IDE', '{', '<VariaveisDaStruct>', '}']];
             
             
# Variaveis do corpo de uma struct
VariaveisDaStruct = [['<DeclaracaoDeVariavelDeStruct>', '<OpcionaisVariaveisDaStruct>']];
OpcionaisVariaveisDaStruct = [['<VariaveisDaStruct>'], []];


# Declaração de variavel dentro de estrutura
DeclaracaoDeVariavelDeStruct = [['<Tipo>', '<ListaDeVariaveisStruct>', ';']];
# Identificaçao da variavel e atribuicaço de valor
ListaDeVariaveisStruct = [['-IDE', '<OpcionalDimensoesDeAcesso>', '<AtribuicaoMultiplaStruct>']]
# listagem e atribuição de outras variaveis
AtribuicaoMultiplaStruct = [['<AtribuicaoDeVariavelStruc>', '<OutrasAtribuicoesOpcionais>']]
# multiplas declarações opcionais
OutrasAtribuicoesOpcionais = [[',', '<ListaDeVariaveisStruct>'], []]
# Valor opcional de atribuiçao
AtribuicaoDeVariavelStruc = [['=', '<ValorDeStribuicaoStruct>'], []]
ValorDeStribuicaoStruct = [['-IDE', '<Valor_Comecando_Com_IDE>', '<VALESSSSXPRESS>'], ['-NRO'], ['-CAC'], ['<Boolean>'], ['(', '<ExpressaoAritmetica>', ')'], ['!', '-IDE', '<Valor_Comecando_Com_IDE>', '<OperadorLogico>', '<Expressao Opcional>']]
           
# elemento de matriz
# elemento de tipo composto
# retorno de função                
Valor_Comecando_Com_IDE = [['<ConteudoDoPrintIDE>'], ['(', '<OpcionaisArgumentos>', ')']]
                           
VALESSSSXPRESS = [['<OperadorLogico>', '<Expressao Opcional>'], []]
                           
# <PossivelExpressaoAritimetica> = <MultiplicacaoOuDivisao> <ExpressaoComSomaSub> |


# Declaração opcional de variáveis globais
OpcionaislVariaveisGlobais = [['<VariaveisGlobais>'], []]
# Bloco de variaveis globais        
VariaveisGlobais = [['var', '{', '<DeclaracaoDentroDoBlocoDeVar>', '}']]
DeclaracaoDentroDoBlocoDeVar = [['<VariaveisDaStruct>']]
                    

# Declaração do opcionais de constantes
OpcionaisConstantes = [['<Constantes>'], []]
# Bloco de constantes
Constantes = [['const', '{', '<DeclaracaoDentroDoBlocoDeConst>', '}']]
DeclaracaoDentroDoBlocoDeConst = [['<VariaveisDaStruct>']]
            

# Area para declaração de funões ou procedimentos
AreaDeFuncoesEProcedimentos = [['<FuncaoOuProcedimento>', '<HasAnotherFuncOrProc>']]
HasAnotherFuncOrProc = [['<AreaDeFuncoesEProcedimentos>'], []]
FuncaoOuProcedimento = [['<Funcao>'], ['<Procedimento>']]
                        

# Bloco
BlocoDeCodigo = [['{', '<Conteudos>', '}']]
Conteudos = [['<ConteudoDeBloco>', '<Conteudos>'], []]
ConteudoDeBloco = [['<While>'], ['<If>'], ['<Print>'], ['<Read>'], ['<VariaveisGlobais>'], ['-IDE', '<VariacoesComIDEnoBloco>']]
  

# Chamada de função ou procedimento
# atribuiçõo de valor em uma variavel
# atribuição de valor em matriz
VariacoesComIDEnoBloco = [['(', '<OpcionaisArgumentos>', ')', ';'],  ['=', '<ValorDeStribuicaoStruct>', ';'], ['<DimensaoDaMatriz>', '=', '<ValorDeStribuicaoStruct>', ';']]
# <AtribuicaoDeValorNoBloco> = 
                   

# While
While = [['while', '(', '<AlgumaDasExpressoes>', ')', '<BlocoDeCodigo>']]
         


# If
If = [['if', '(', '<AlgumaDasExpressoes>', ')', 'then', '<ConteudoDoIf>']]
ConteudoDoIf = [['<BlocoDeCodigo>', '<OpcionalElse>']]
OpcionalElse = [['else', '<BlocoDeCodigo>'], []]
                


# Elemento de matriz
# <ElementoDaMatriz> = IDE <DimensaoDaMatriz>
DimensaoDaMatriz = [['<IndiceDeAcessoDaMatriz>', '<OpcionalIndice>']]
IndiceDeAcessoDaMatriz = [['[', '<ValorDoIndice>', ']']]
OpcionalIndice = [['<IndiceDeAcessoDaMatriz>', '<OpcionalIndice>'], []]           
ValorDoIndice = [['-NRO'], ['-IDE']]
           

#! Print
Print = [['print', '(', '<ConteudoDoPrint>', ')', ';']]
ConteudoDoPrint = [['-IDE', '<ConteudoDoPrintIDE>'], ['-CAC']]
ConteudoDoPrintIDE = [['.', '-IDE'], ['<DimensaoDaMatriz>'], []]
                      

#! Read
Read = [['read', '(', '<Ler>', ')', ';']]
Ler = [['-IDE', '<ConteudoDoPrintIDE>']]
       

#! Chamada funcção
#! <RetornoFuncao> = IDE '(' <OpcionaisArgumentos> ')'
OpcionaisArgumentos = [['<ListaDeArgumentos>'], []]
ListaDeArgumentos = [['<Argumento>', '<OutrosArgumentos>']]
OutrosArgumentos = [[',', '<ListaDeArgumentos>'], []]
Argumento = [['<ValorDeStribuicaoStruct>']]

#! Ou também chamada de procedimento
#! <ChamadaFuncao> = <RetornoFuncao> ';'


#! Expressao Aritmetica
ExpressaoAritmetica = [['<ValorOuMultiDiv>', '<ExpressaoComSomaSub>']]
ValorOuMultiDiv = [['<Valor>', '<MultiplicacaoOuDivisao>']]
MultiplicacaoOuDivisao = [['*', '<ValorOuMultiDiv>'],  ['/', '<ValorOuMultiDiv>'], []]
ExpressaoComSomaSub = [['<SimboloSomaSub>', '<ExpressaoAritmetica>'], []]
Valor = [['<Operavel>'], ['(', '<ExpressaoAritmetica>', ')']]
SimboloSomaSub = [['+'], ['-']]
Operavel = [['-IDE', '<Valor_Comecando_Com_IDE>'], ['-NRO']]
            

#! Expressão logica
#! <NegacaoLogica> = '!' IDE <Valor_Comecando_Com_IDE>
ExpressaoLogica = [['<neg>', '<OperadorLogico>', '<Expressao Opcional>']]
ExpressaoOpcional = [['<op>', '<neg>', '<Expressao Opcional>'], []]
op = [['&&'],  ['||'] ]    
#! negação ou variavel contendo valor booleano 
neg = [['<Negacao>'],  ['-IDE', '<Valor_Comecando_Com_IDE>'],  ['(', '<ExpressaoLogica>', ')']]
OperadorLogico = [['&&','<neg>'],  ['||', '<neg>']]
Negacao = [['!', '-IDE', '<Valor_Comecando_Com_IDE>']]
          


#! Expressaõ relacional
ExpressaoRelacional = [['<OperandoRelacional>', '<REL>', '<OperandoRelacional>', '<EXP_REL_Opcional>']]
EXP_REL_Opcional = [['<REL>', '<ExpressaoRelacional>'], []]
OperandoRelacional = [['<ValorDeStribuicaoStruct>'], ['(', '<ExpressaoRelacional>', ')']]

#! Se começar com negção então é logica
AlgumaDasExpressoes = [
  ['!', '-IDE', '<Valor_Comecando_Com_IDE>', '<OperadorLogico>', '<Expressao Opcional>'], 
  ['-IDE', '<Valor_Comecando_Com_IDE>', '<ADE_com_IDE_VALOR>'],
  ['-NRO', '<REL>', '<OperandoRelacional>',' <EXP_REL_Opcional>'],
  ['-CAC', '<REL>', '<OperandoRelacional>', '<EXP_REL_Opcional>'],
  ['<Boolean>', '<ADE_com_Bool>'],
]
     
#! expressao logica ou                   
ADE_com_IDE_VALOR = [['<OperadorLogico>', '<Expressao Opcional>'], ['<REL>', '<OperandoRelacional>', '<EXP_REL_Opcional>']]
ADE_com_Bool = [['<REL>', '<OperandoRelacional>', '<EXP_REL_Opcional>'], []]
#!<ADE_com_parenteses> = IDE <Valor_Comecando_Com_IDE> <ADE_com_IDE_VALOR>   
#!                       | NRO <REL> <OperandoRelacional> <EXP_REL_Opcional>
#!                       | CAC <REL> <OperandoRelacional> <EXP_REL_Opcional>
#!                       | <Boolean> <ADE_com_Bool>


#! Declaração de uma função                        
Funcao = [['function', '<Tipo>', '-IDE', '(', '<ListParametros>', ')', '<BlocoDeCodigo>']]
#! Lista de parametros pode ser vazia
ListParametros = [['<Parametro>', '<OutroParametro>'], []]
#! Se mais de um parametro
OutroParametro = [[',', '<ListParametros>'], []]
#! Definição do parametro
Parametro = [['<Tipo>', '-IDE']]
             
#! Tipo
Tipo = [['int'], ['real'], ['boolean'], ['string'], ['-IDE']]
#! Declaração de um procedimento
Procedimento = [['procedure', '-IDE', '(', '<ListParametros>', ')', '<BlocoDeCodigo>']]

Mapped = Dict[str, ProductionRules]

map: Mapped = {
  '<EstruturaDoPrograma>': EstruturaDoPrograma,
  '<Boolean>': Boolean,
  '<OpcionalDimensoesDeAcesso>' : OpcionalDimensoesDeAcesso,
  '<DimensoesDeAcesso>': DimensoesDeAcesso,
  '<TamanhoDaDimensao>': TamanhoDaDimensao,
  '<DimensaoOpcional>': DimensaoOpcional,
  '<IndiceDeAcesso>': IndiceDeAcesso,
  '<OpcionalStruct>': OpcionalStruct,
  '<DeclaracaoStruct>': DeclaracaoStruct,
  '<CorpoDaEstrutura>': CorpoDaEstrutura,
  '<EspecializacaoDeStruct>': EspecializacaoDeStruct,
  '<VariaveisDaStruct>': VariaveisDaStruct,
  '<OpcionaisVariaveisDaStruct>': OpcionaisVariaveisDaStruct,
  '<DeclaracaoDeVariavelDeStruct>': DeclaracaoDeVariavelDeStruct,
  '<ListaDeVariaveisStruct>': ListaDeVariaveisStruct,
  '<AtribuicaoMultiplaStruct>': AtribuicaoMultiplaStruct,
  '<OutrasAtribuicoesOpcionais>': OutrasAtribuicoesOpcionais,
  '<AtribuicaoDeVariavelStruc>': AtribuicaoDeVariavelStruc,
  '<ValorDeStribuicaoStruct>': ValorDeStribuicaoStruct,
  '<Valor_Comecando_Com_IDE>': Valor_Comecando_Com_IDE,
  '<VALESSSSXPRESS>': VALESSSSXPRESS,
  '<OpcionaislVariaveisGlobais>': OpcionaislVariaveisGlobais,
  '<VariaveisGlobais>': VariaveisGlobais,
  '<DeclaracaoDentroDoBlocoDeVar>': DeclaracaoDentroDoBlocoDeVar,
  '<OpcionaisConstantes>': OpcionaisConstantes,
  '<Constantes>': Constantes,
  '<DeclaracaoDentroDoBlocoDeConst>': DeclaracaoDentroDoBlocoDeConst,
  '<AreaDeFuncoesEProcedimentos>': AreaDeFuncoesEProcedimentos,
  '<FuncaoOuProcedimento>': FuncaoOuProcedimento,
  '<BlocoDeCodigo>': BlocoDeCodigo,
  '<Conteudos>': Conteudos,
  '<ConteudoDeBloco>': ConteudoDeBloco,
  '<VariacoesComIDEnoBloco>': VariacoesComIDEnoBloco,
  '<While>': While,


  '<If>': If,
  '<ConteudoDoIf>': ConteudoDoIf,
  '<OpcionalElse>': OpcionalElse,
  '<DimensaoDaMatriz>': DimensaoDaMatriz,
  '<IndiceDeAcessoDaMatriz>': IndiceDeAcessoDaMatriz,
  '<OpcionalIndice>': OpcionalIndice,
  '<ValorDoIndice>': ValorDoIndice,
  '<Print>': Print,
  '<ConteudoDoPrint>': ConteudoDoPrint,
  '<ConteudoDoPrintIDE>': ConteudoDoPrintIDE,
  '<Read>': Read,
  '<Ler>': Ler,
  '<OpcionaisArgumentos>': OpcionaisArgumentos,
  '<ListaDeArgumentos>': ListaDeArgumentos,
  '<OutrosArgumentos>': OutrosArgumentos,
  '<Argumento>': Argumento,
  '<ExpressaoAritmetica>': ExpressaoAritmetica,
  '<ValorOuMultiDiv>': ValorOuMultiDiv,
  '<MultiplicacaoOuDivisao>': MultiplicacaoOuDivisao,
  '<ExpressaoComSomaSub>': ExpressaoComSomaSub,
  '<Expressao Opcional>': ExpressaoOpcional,

  '<Valor>': Valor,
  '<SimboloSomaSub>': SimboloSomaSub,
  '<Operavel>': Operavel,
  '<ExpressaoLogica>': ExpressaoLogica,
  '<ExpressaoOpcional>': ExpressaoOpcional,
  '<op>': op,
  '<neg>': neg,
  '<OperadorLogico>': OperadorLogico,
  '<Negacao>': Negacao,
  '<ExpressaoRelacional>': ExpressaoRelacional,
  '<EXP_REL_Opcional>': EXP_REL_Opcional,
  '<OperandoRelacional>': OperandoRelacional,
  '<AlgumaDasExpressoes>': AlgumaDasExpressoes,
  '<ADE_com_IDE_VALOR>': ADE_com_IDE_VALOR,
  '<ADE_com_Bool>': ADE_com_Bool,
  '<Funcao>': Funcao,
  '<ListParametros>': ListParametros,
  '<OutroParametro>': OutroParametro,
  '<Parametro>': Parametro,
  '<Tipo>': Tipo,
  '<Procedimento>': Procedimento,
  '<HasAnotherFuncOrProc>': HasAnotherFuncOrProc,
  '<REL>': REL,
};
