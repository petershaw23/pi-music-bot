from time import sleep      # Importing the time library to provide the delays in program
#sleep (10)
import subprocess
import os
import random
import time
import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot

# print(os.environ) #test 

import pibot_token # imports local file pibot-token.py with telegram bot token
token = pibot_token.token

import IDList # imports local file IDList.py with allowed telegram users
IDList = IDList.IDList
#IDList = [32089472] #for testing
#print(IDList)

import IPs # imports local file IPs.py with LAN IP Addresses
kodi_IP = IPs.kodi_IP
plug_kodi_IP = IPs.plug_kodi_IP



def handle(msg):
    
    def logging(status):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print (str(timestamp) +': '+str(command)+' sent by ID# '+str(sender)+': '+str(status))
    
    
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']['id']
    
    if sender in IDList:
        logging('allowed!')
        
 
        if command == '/start':
            bot.sendMessage (chat_id, str("Hi! Dies ist dem Michael sein toller Pi-Bot! Versuche mal /time /date oder /roll !"))
        elif command == '/time':
            now = datetime.datetime.now() # Getting date and time
            bot.sendMessage(chat_id, str(now.hour) + str(":") + str(now.minute), parse_mode= 'Markdown')
        elif command == '/date':
             now = datetime.datetime.now() # Getting date and time
             bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
        elif command == '/roll':
            bot.sendMessage(chat_id, random.randint(1,6))
       
    
    
   
    else:
        bot.sendMessage(chat_id, 'access denied! you suck, ID# '+str(sender))
        logging('DENIED!')
        
bot = telepot.Bot(token) # get token key from from local file pibot-token.py
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)
