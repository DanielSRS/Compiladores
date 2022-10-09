

<!-- PROJECT LOGO -->
## Sobre o projeto
Um analizador léxico para uma pseudo linguagem de programação escrito em python.

A entrada para este analisador é um conjunto de arquivos texto que será processado de acordo com a estrutur léxica da linguagem e dará como saída um conjunto de arquivos de saída apresentando a lista de tokens, proveniente da análise léxica, além dos erros léxicos, caso existam.
<br />

<br>

<!-- TABLE OF CONTENTS -->

## Tabela de Conteúdo

- [Sobre o Projeto](#sobre-o-projeto)
- [Tabela de Conteúdo](#tabela-de-conte%C3%BAdo)
- [Feito Com](#feito-com)
- [Começando](#come%C3%A7ando)
  - [Pré-requisitos](#pr%C3%A9-requisitos)
  - [Estrutura de Arquivos](#estrutura-de-arquivos)
  - [Instalação](#instala%C3%A7%C3%A3o)
  - [Linting](#edi%C3%A7%C3%A3o)
  - [Edição](#edi%C3%A7%C3%A3o)
  - [Executar projeto](#executar-projeto)
- [Contribuição](#contribui%C3%A7%C3%A3o)

<!-- ABOUT THE PROJECT -->

<br>

## Feito Com

Abaixo segue o que foi utilizado na criação deste projeto:

- [Python](https://www.python.org/) - Python é uma linguagem de programação que permite trabalhar rapidamente
e integrar os sistemas de forma mais eficaz.

<br>

<!-- GETTING STARTED -->

## Começando

Para conseguir rodar o projeto, siga os passos abaixo.

### Pré-requisitos

Antes de seguirmos, é preciso que você tenha o ambiente configurado para criar e testar aplicações em Python. Caso não tenha o python3 instalado na sua maquina, verifique como pode instalar na sua plataforma seguindo as instruções disponíveis na pagina do projeto: [Python.org](https://www.python.org/)

### Estrutura de Arquivos

A estrutura de arquivos está da seguinte maneira:

```bash
Compiladores
├── .vscode/
├── entrada/
├── saida/
├── src/
│   ├── automata/
│   │   └── automataName.py
│   ├── TokenUtils/
│   │   └── utilityName.py
│   ├── filesystem.py
│   └── main.py
├── .gitignore
└── README.md
```

Serão explicados os arquivos e diretórios na seção de [Edição](#edição).

### Instalação

1. Clone o projeto utilizando o comando:

```sh
$ git clone https://github.com/DanielSRS/Compiladores
```

2. Navegue para o diretorio raiz do projeto e crie as pastas nescessárias para execução com o camando:

```sh
$ cd Compiladores
$ mkdir entrada
$ mkdir saida
```

### Linting
O codigo do projeto é tipado. Esta etapa não é nescessária, mas para ter uma melhor experiencia habilite linting no seu editor de preferencia, e defina a verificação de tipos como 'strict'
<br>
<br>
Se você usa o Visual Studio Code como editor não precisa fazer nada.

<br>

### Edição

Nesta seção haverão instruções caso você queira editar o projeto, explicando para que os diretórios são utilizados e também os arquivos de configuração.

- **.vscode** - Arquivos de configuração do Visual Studio Code. Esses arquivos não são nescessarios caso você não use o VS Code como editor. São apenas as configurações descritas nas seção de [Linting](#linting).

- **entrada** - Diretório contendo todos os arquivos fonte que irão ser processdos pelo analizador léxido. Se não houver nenhum arquivo, não será produzido nenhum arquivo de saíde após execução. Se diretório estiver ausente, um erro acontecerá ao executar o projeto.

- **saida** - Após execução do projeto, o analizador léxico irá gerar arquivos de saída neste diretório contendo as informações processadas em cada arquivo de entrada.

- **src** - Diretório contendo todos os arquivos da aplicação, é criado um diretório `src` para que o código da aplicação possa ser isolado em um diretório e facilmente portado para outros projetos, se necessário.

  - **automata** - A python package onde estão agrupados todos os automatos para processamento de lexemas e funções relacionadas

  - **tokenUtils** - A python package onde estão agrupados todos modulos para geração, processamento e manipulação de tokens além de funções relacionadas;

  - **main.py** - Arquivo responsável por centralizar o código do diretório `src`, aqui são realizadas as operções principais de abertura leitura dos arquivos de codigo fonte (presentes no arquivo de entrda) e gravação da lista de token nos arquivos de saída (no diretório 'saida').

  - **filesystem.py** - Operações relacionadas ao sistema de arquivos, como a abertura e leitura de arquivos;


- **.gitignore** - Arquivo de configurção do git contendo informções de arquivos que não devem ser versionados junto com o codigo fonte;

- **README.md** -  Este arquivo. Aqui é feito a documentação basica do projeto com instruções de instalação, configuração e execução.

## Executar projeto

- Ainda no diretório raiz:

  ```sh
  $ python3 src/main.py
  ```
- Varifique a saida no diretório 'saida'

<br>

## Contribuição

- Quaisquer dúvidas, sugestões ou problemas que encontrar, fique livre para abrir uma issue.
- Se quiser contribuir ajustando o codigo, implementando novas funcionalidas ou corrigindo bugs, faça um fork do projeto, faça as alterações nescessárias como descrito na seção de [Edição](#edição) e abra um pull request
