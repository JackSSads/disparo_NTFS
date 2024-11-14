from re import search
from pdfplumber import open as pdf_open

from utils import DiretoriosArquivos
from service import DisparoEmail

from datetime import datetime
from typing import Union

diretorios = DiretoriosArquivos()
email = DisparoEmail()

class AutomacaoDesk():
    def __init__(self):
        pass

    def extrair_zip(self, path_arquivo: str, path_destino: str) -> str:
        novo_path_arquivo = diretorios.renomear_arquivo(path_arquivo=path_arquivo, novo_nome='NTFS.zip')
        path_arquivo_extraido = diretorios.extrair_pdf(path_arquivo=novo_path_arquivo, path_busca=path_destino)

        return path_arquivo_extraido
        
    def separar_arquivos(self, path_file_extrated: str) -> Union[list, None]:
        # buscando o diretório onde estão os arquivos
        path_completo, arquivos = diretorios.listar_arquivos(path_busca=path_file_extrated)

        # separando os arquivos por pastas
        notas = diretorios.listar_arquivos(path_busca=f"{path_completo}\\{arquivos[0]}")

        lista_path_notas = []

        for nota in notas[1]:
            data = ""
            if "EXTRATO PGDAS" in nota or "PGDAS" in nota:
                extrato_pgdas = r"(EXTRATO PGDAS)\s(\d{2}\s\d{4})\s-\s(.*)"
                pgdas = r"(PGDAS)\s(\d{2}\s\d{4})\s-\s(.*)"

                resultado_extrato_pgdas = search(extrato_pgdas, nota)
                resultado_pgdas = search(pgdas, nota)

                if resultado_extrato_pgdas:
                    data = resultado_extrato_pgdas.group(2)

                    # Mover para a encargos\\mes
                    diretorios.mover_arquivo(
                        path_arquivo=f"{path_completo}\\{arquivos[0]}\\{nota}",
                        path_destino=f"Desktop\\Robotic\\Encargos\\{data}"
                    )
                
                elif resultado_pgdas:
                    data = resultado_pgdas.group(2)

                    # Mover para a encargos\\mes
                    diretorios.mover_arquivo(
                        path_arquivo=f"{path_completo}\\{arquivos[0]}\\{nota}",
                        path_destino=f"Desktop\\Robotic\\Encargos\\{data}"
                    )

            elif "NFS-E" in nota:
                try:
                    empresa = ""

                    if data == "":
                        data = str(datetime.now().strftime("%m/%Y")).replace("/", " ")

                    # Abre o arquivo PDF
                    with pdf_open(f"{path_completo}\\{arquivos[0]}\\{nota}") as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            
                            # Verifica se o texto "Nome/Razão Social" está na página
                            if "Nome/Razão Social" in text:
                                # Extrai o conteúdo depois do texto
                                start = text.find("Nome/Razão Social") + len("Nome/Razão Social:")
                                razao_social = text[start:].split("\n")[0].strip()
                                empresa = str(razao_social)

                    # Mover para a Clientes\\Empresa\\Data
                    home_path = diretorios.mover_arquivo(
                        path_arquivo=f"{path_completo}\\{arquivos[0]}\\{nota}", 
                        path_destino=f"Desktop\\Robotic\\Clientes\\{empresa}\\{data}"
                    )
                    
                    dados_empresa = {
                        "empresa": empresa,
                        "path_arquivo": home_path
                    }
                    
                    lista_path_notas.append(dados_empresa)

                except AttributeError as e:
                    print(f"Erro ao acessar o grupo: {e}")
                    return None

        return lista_path_notas
    
    def enviar_arquivos(self, lista_path_notas: list) -> None:

        lista_emails_empresas = {
            "IDATHA BUSINESS INTELLIGENCE LTDA": "jackson@adaupsoft.com",
            "TRIAD INTEGRATION SERVICOS E TECNOLOGIA DA INFORMACAO LTDA.": "jackson@adaupsoft.com"
        }

        for empresa in lista_path_notas:

            print(f"Enviando {empresa['path_arquivo']} para {empresa['empresa']}")         
            email.enviar_email(file_path=empresa["path_arquivo"],  email_empresa=lista_emails_empresas[empresa["empresa"]])
            
            print("Enviado com sucesso!")
        return None
        
    def gerenciador(self, path_arquivo: str, path_destino_arquivo_extraido: str, path_download_notas: str) -> None:
        
        path_arquivo_extraido = self.extrair_zip(
            path_arquivo=path_arquivo, 
            path_destino=path_destino_arquivo_extraido
        )

        diretorios.remover_diretorio(remover_path=path_download_notas)
        
        lista_path_notas = self.separar_arquivos(path_file_extrated=path_arquivo_extraido)
        
        self.enviar_arquivos(lista_path_notas=lista_path_notas)

        diretorios.remover_diretorio(remover_path=path_destino_arquivo_extraido)