from whatsapp_api import WhatsAppApi
from time import sleep
import os

wp = WhatsAppApi()
wp.sign_site('https://web.whatsapp.com/')
wp.search_contact('5512981209167')

# mensagens = ['olá como vai', 'e vc como está ', 'isso é um teste', 'ok entende ', 'quantas mensagem posso receber','hum entendi']
#
# for m in mensagens:
#     wp.send_message(m)
#     sleep(2)

path = os.getcwd()
file = path + '/video.mp4'
wp.send_media(file)

wp.close()
