from selenium import webdriver
from time import sleep
import os

## XPATHS
CONTACTS = '//*[@id="main"]/header/div[2]/div[2]/span'
SEND = '//*[@id="main"]/footer/div[1]/div[3]/button'
MESSAGE_BOX = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
NEW_CHAT = '//*[@id="side"]/header/div[2]/div/span/div[2]/div'
SEARCH_CONTACT = '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/input'
FIRST_CONTACT = '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div'
SEND_MEDIA = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div'


class WhatsAppApi:

    def __init__(self):
        self.driver_path = os.getcwd() + "/chromedriver"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=Perfil')
        self.chrome = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def sign_site(self, url):
        self.chrome.get(url)
        # espera 15 segundo para o html ser renderizado
        sleep(20)
        # input("Depois de logar aperte ENTER, para continuar a aplicação")

    def _get_element(self, xpath, attempts=5, _count=0):
        '''Pega elemento do Dom com multiplas tentativas'''
        try:
            element = self.chrome.find_element_by_xpath(xpath)
            print('Elemento encontrado!')
            return element
        except Exception as e:
            if _count < attempts:
                sleep(1)
                print(f'Tentativa {_count}')
                self._get_element(xpath, attempts=attempts, _count=_count + 1)
            else:
                print("Elemento não encontrado" + e)

    def _click(self, xpath):
        sleep(1)
        el = self._get_element(xpath)
        el.click()

    def _send_keys(self, xpath, message):
        el = self._get_element(xpath)
        el.send_keys(message)

    def _write_message(self, message):
        '''Escreve a mensagem de texto na caixa de entrada mais não envia'''
        self._click(MESSAGE_BOX)
        self._send_keys(MESSAGE_BOX, message)

    def send_message(self, message):
        '''escreve e envia a mensagem'''
        self._write_message(message)
        sleep(3)
        self._click(SEND)

    def send_media(self, fileToSend):
        """ Envia media """
        try:
            # Clica no botão adicionar
            self.chrome.find_element_by_css_selector("span[data-icon='clip']").click()
            # Seleciona input
            attach = self.chrome.find_element_by_css_selector("input[type='file']")
            # Adiciona arquivo
            attach.send_keys(fileToSend)
            sleep(30)
            self._click(SEND_MEDIA)
            sleep(35)
        except Exception as e:
            print("Erro ao enviar media", e)

    def get_group_numbers(self):
        '''Pega número de constatos de um grupo'''
        try:
            el = self.chrome.find_element_by_xpath(CONTACTS)
            return el.text.split(',')
        except Exception as e:
            print("número não encontrado" + e)

    def search_contact(self, keyword):
        '''pesquisa por contato'''
        self._click(NEW_CHAT)
        self._send_keys(SEARCH_CONTACT, keyword)
        sleep(1)
        try:
            self._click(FIRST_CONTACT)
        except Exception as e:
            print("contato não encontrado" + e)

    def close(self):
        sleep(10)
        self.chrome.close()

