from zipfile import ZipFile
from typing import Union
import shutil
from os import path, name, makedirs, system, walk, rename, listdir

class DiretoriosArquivos():
    def __init__(self):
        self.path_base = path.expanduser('~') # C:Users\Jack\

    def verifica_se_diretorio_existe(self, path_busca: str, oculto: bool = False) -> tuple:
        path_completo = path.join(self.path_base, path_busca)

        if path.exists(path_completo):
            print(f"Diretório \033[32m{path_busca}\033[m encontrado")
            return (path_completo, path_busca)
        else:
            print(f"Diretório {path_busca} não existe\nCriando diretório...")
            makedirs(path_completo, exist_ok=True)
            
            if oculto and name == 'nt':
                system(f'attrib +h "{path_completo}"')

            return (path_completo, path_busca)

    def extrair_pdf(self, path_arquivo: str, path_busca: str) -> Union[str, None]:
        path_destino_completo = self.verifica_se_diretorio_existe(path_busca)

        # Verifica se o arquivo existe
        if path.exists(path_arquivo):
            with ZipFile(path_arquivo, 'r') as zip_ref:
                zip_ref.extractall(path_destino_completo[0])
            print(f'Arquivo descompactado em: {path_destino_completo[0]}')
            return path_destino_completo[0]
        else:
            print('Arquivo zip não encontrado.')
            return None

    def remover_diretorio(self, remover_path: str) -> Union[tuple, None]:
        path_completo = path.join(self.path_base, remover_path)

        print(f"Removendo o diretório: {path_completo}")

         #Verifica se o diretório existe e o remove, mesmo que contenha arquivos
        if path.exists(path_completo):
            shutil.rmtree(path_completo)
            print(f'O diretório \033[32m{remover_path}\033[m excluído: {path_completo}')
            
            return (path_completo, remover_path)
        else:
            print(f'Diretório não encontrado: {path_completo}')
            return None

    def renomear_arquivo(self, path_arquivo: str, novo_nome: str) -> Union[str, None]:
        path_completo = path.join(self.path_base, path_arquivo)
        
        if path.exists(path_completo):
            for raiz, diretorios, arquivos in walk(path_completo):
                for arquivo in arquivos:
                    # Cria o caminho completo para o arquivo
                    antigo_path_arquivo = path.join(raiz, arquivo)
                    # Cria um novo caminho para o arquivo renomeado
                    novo_path_arquivo = path.join(raiz, novo_nome)
                    
                    # Verifica se o novo nome já existe
                    if path.exists(novo_path_arquivo):
                        print(f'Erro: O arquivo \033[31m{novo_nome}\033[m já existe em \033[31m{raiz}\033[m.')
                        continue

                    # Renomeia o arquivo
                    rename(antigo_path_arquivo, novo_path_arquivo)
                    print(f'Arquivo renomeado de \033[32m{arquivo}\033[m para \033[32m{novo_nome}\033[m\nNovo caminho: {novo_path_arquivo}')
                    return novo_path_arquivo
            return novo_path_arquivo
        else:
            print(f'Diretório não encontrado: {path_completo}')
            return None
        
    def listar_arquivos(self, path_busca: str) -> Union[tuple, None]:
        path_completo = path.join(self.path_base, path_busca)
        if path.exists(path_completo):
            # Lista os arquivos do diretório
            files: list = listdir(path_completo)
            return (path_completo, files)
        else:
            print(f'Diretório não encontrado: {path_completo}')
            return None
    
    def mover_arquivo(self, path_arquivo: str, path_destino: str) -> Union[tuple, None]:
        path_completo = path.join(self.path_base, path_arquivo)

        if path.exists(path_completo):
            # Cria o novo caminho para o arquivo
            novo_path_arquivo = self.verifica_se_diretorio_existe(path_busca=path_destino)

            # Verifica se o arquivo de destino já existe
            path_final_destino = path.join(novo_path_arquivo[0], path.basename(path_arquivo))

            if path.exists(path_final_destino):
                print(f'Arquivo já existe em \033[31m{novo_path_arquivo[0]}\033[m.')
                return path_final_destino
            else:
                # Move o arquivo para o novo caminho
                shutil.move(path_completo, path_final_destino)

                print(f'Arquivo movido de \033[32m{path_arquivo}\033[m para \033[32m{path_destino}\033[m\nNovo caminho: {novo_path_arquivo}')
                return path_final_destino
        else:
            print(f'Arquivo não encontrado em: {path_completo}')
            return None