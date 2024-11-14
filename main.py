from bots import BuscarNotasEmail
from resources import AutomacaoDesk
from utils import DiretoriosArquivos

web = BuscarNotasEmail()
desktop = AutomacaoDesk()
diretorios = DiretoriosArquivos()

def main():
    path_completo, path_verifiado = diretorios.verifica_se_diretorio_existe(
        path_busca="Downloads\\Notas",
        oculto=True
    )
    
    web.gerenciador()

    desktop.gerenciador(
        path_arquivo=path_verifiado,
        path_destino_arquivo_extraido='Desktop\\Robotic\\Notas',
        path_download_notas=path_verifiado
    )
    
main()