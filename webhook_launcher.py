import requests
import os, time, config

def telegram_bot_sendtext(bot_message):
    
    bot_token = '5004712342:AAEh0rTB5dWhlx_YITgDeDyX2awN8g3JLEM'
    bot_chatID = '-667139609'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


 
 


