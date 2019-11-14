from time import sleep      # Importing the time library to provide the delays in program
#sleep (10)
import subprocess
import os
import random
import time
import datetime  # Importing the datetime library
timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
print (timestamp)
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot



import pibot_token # imports local file pibot-token.py with telegram bot token
token = pibot_token.token

import IDList # imports local file IDList.py with allowed telegram users
IDList = IDList.IDList
print(IDList)

import IPs # imports local file IPs.py with LAN IP Addresses
kodi_IP = IPs.kodi_IP
plug_kodi_IP = IPs.plug_kodi_IP



def handle(msg):
    
    def logging():
        print (str(timestamp) +': Message '+str(command)+' sent by ID# '+str(sender))
    
    
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']['id']
    
    if sender in IDList:
        bot.sendMessage(chat_id, 'access granted, you are ID# '+str(sender))
        logging()
        if command == 'hi':
            bot.sendMessage(chat_id, 'hi, '+str(sender))
            logging()
        
    else:
        bot.sendMessage(chat_id, 'access denied! you suck, ID# '+str(sender))
        logging()
        
bot = telepot.Bot(token) # get token key from from local file pibot-token.py
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)
