from time import sleep      # Importing the time library to provide the delays in program
#sleep (10)
import subprocess
import os
import random
import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot



import pibot_token # imports local file pibot-token.py with telegram bot token
token = pibot_token.token

import IPs
kodi_IP = IPs.kodi_IP
plug_kodi_IP = IPs.plug_kodi_IP


id_a = [111111,2222222,3333333,4444444,5555555]

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']['id']
    if sender in id_a:
        bot.sendMessage(chat_id, 'allow access!')
    else:
        bot.sendMessage(chat_id, 'Forbidden access!')
        bot.sendMessage(chat_id, sender)
 
    
bot = telepot.Bot(token) # get token key from from local file pibot-token.py
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)
