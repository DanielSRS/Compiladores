from os import listdir
from os.path import isfile, join


"""
  Lista todos os arquivos de um dado diretorio

  Retorna um lista de strings com os nomes dos arqivos
"""
def listDirFiles(dirPath: str) -> 'list[str]': 
  onlyfiles = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
  return onlyfiles;

