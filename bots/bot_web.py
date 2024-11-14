from utils.webdriver_selenium import Driver
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = Driver(time_wait=120)

class BuscarNotasEmail():
    def __init__(self):
        pass

    def login_email(self, email: str, senha: str) -> None:

        driver.initialize_webdriver()

        # Navegando para a página de login do Zoho Mail
        print("Acessando o Zoho Mail")
        driver.navigate_to("https://accounts.zoho.com/signin?service_language=pt&servicename=VirtualOffice&signupurl=https://www.zoho.com/pt-br/mail/zohomail-pricing.html&serviceurl=https://mail.zoho.com")

        # Escrevendo e-mail
        input_email = driver.waiting("//input[@id='login_id']")
        print("Escrevendo e-mail")
        driver.write(element=input_email, text=email)

        # Procurando o botão de "Próximo"
        print("Clicando em Próximo")
        driver.waiting("//button[@id='nextbtn']").click()

        # Escrevendo senha
        input_senha = driver.waiting("//input[@id='password']")
        print("Escrevendo senha")
        driver.write(element=input_senha, text=senha)

        # Procurando o botão de "Próximo"
        print("Clicando em Próximo")
        driver.waiting("//button[@id='nextbtn']").click()

    def buscar_notas(self) -> None:
        # Buscar input de busca
        print("Esperando o input de busca")
        input_busca = driver.waiting("//input[@class='zmSearchTB js-searchbox']")
        print("Digitando no campo busca")
        driver.write(element=input_busca, text="isaiasmarques07@gmail.com")

        # Pressionando Enter para buscar
        print("Pressionando Enter para buscar")
        driver.keys(element=input_busca, key=Keys.ENTER)

        # Pressionando ESC para sair da busca        
        print("Saindo da busca")
        driver.keys(element=input_busca, key=Keys.ESCAPE)

        # entrando no email
        sleep(2)        
        print("Acessando o primeiro email")
        driver.waiting("//div[@class='SCm']//div[@class='zmAppContent']/div/div[1]").click()

        # Clicando no botão Fazer download
        sleep(2)
        print("Clicando no botão Fazer download")
        driver.waiting("//div[@class='SCm']//div[@id='zmAttachWra']/div/div/div[2]/div/button[2]").click()

        # Garantindo que o download foi concluído
        sleep(5)
        print("Download concluído")
   
    def gerenciador(self) -> None:
        self.login_email(email="", senha="")
        result = self.buscar_notas()
        driver.close_web_driver()

        return result
