from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from .seguranca import decrypt_password
import smtplib
import ssl

from datetime import datetime
from dateutil.relativedelta import relativedelta

class DisparoEmail:
    def __init__(self) -> None:
        self.__SMTP_SERVER = "smtp.zoho.com"
        self.__SMTP_PORT = 587
        self.__SENDER_EMAIL = ""
        self.__PASSWORD = ""

    def enviar_email(self, file_path: str, email_empresa: str) -> None:

        # Obter a data atual
        data_atual = datetime.now() - relativedelta(months=1)

        # Calcular o mês anterior
        mes_anterior = data_atual.strftime("%m %Y")

        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Notificação de Importação</title>
            <style>
                body {{
                    background-color: #28a745; /* Fundo verde */
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100dvh; /* Altura total da tela */
                }}
                .card {{
                    background-color: #ffffff; /* Fundo do card */
                    padding: 20px;
                    margin-top: 50px;
                    margin-bottom: 50px;
                    border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    width: 300px; /* Largura do card */
                    text-align: center;
                }}
                .party-name {{
                    font-size: 24px; /* Tamanho da fonte do nome do partido */
                    font-weight: bold;
                    color: #333; /* Cor do texto */
                    margin-bottom: 15px;
                }}
                .message {{
                    font-size: 16px; /* Tamanho da fonte da mensagem */
                    color: #555; /* Cor do texto */
                    margin-bottom: 10px;
                }}
                .dados-cliente {{
                    margin-top: 20px;
                    border-top: 1px solid #ccc;
                    padding-top: 10px;
                    text-align: left;
                }}
                .dados-cliente h5 {{
                    font-size: 18px; /* Tamanho da fonte do título */
                    font-weight: bold;
                    color: #333; /* Cor do texto */
                    margin-bottom: 5px;
                }}
                .dados-cliente ul {{
                    list-style: none;
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="party-name">NFS-E</div>
                <div class="message">
                    <p>Nota fiscal referente ao mês {mes_anterior} está disponível para download.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Criação do e-mail
        message = MIMEMultipart()
        message['From'] = self.__SENDER_EMAIL
        message['To'] = email_empresa
        message['Subject'] = f'Nota fiscal referente ao mês {mes_anterior} está disponível para download.'

        # Anexando o corpo do e-mail
        message.attach(MIMEText(html_content, 'html'))

        # Lendo e anexando o arquivo
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        # Codificar o arquivo em base64
        encoders.encode_base64(part)

        # Adicionar cabeçalhos ao arquivo anexo
        part.add_header(
            'Content-Disposition',
            f'attachment; filename=NFS-E {mes_anterior}.pdf',  # Nome do arquivo
        )

        # Anexar o arquivo ao e-mail
        message.attach(part)

        # Criação do contexto SSL
        context = ssl.create_default_context()
        
        dec = decrypt_password(self.__PASSWORD)

        # Envio do e-mail
        with smtplib.SMTP(self.__SMTP_SERVER, self.__SMTP_PORT) as server:
            server.starttls(context=context)  # Inicia o TLS
            server.login(self.__SENDER_EMAIL, dec)
            server.sendmail(self.__SENDER_EMAIL, email_empresa, message.as_string())