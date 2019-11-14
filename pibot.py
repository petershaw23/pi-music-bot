from time import sleep      # Importing the time library to provide the delays in program
sleep (11)
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
            bot.sendMessage (chat_id, str("Hi! Dies ist dem Michael sein toller Pi-Bot! Versuche mal /time /date /uptime oder /roll !"))
        elif command == '/time':
            now = datetime.datetime.now() # Getting date and time
            bot.sendMessage(chat_id, str(now.hour) + str(":") + str(now.minute), parse_mode= 'Markdown')
        elif command == '/date':
             now = datetime.datetime.now() # Getting date and time
             bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
        elif command == '/roll':
            bot.sendMessage(chat_id, random.randint(1,6))
        elif command == '/uptime':
            with open('/proc/uptime', 'r') as f:
                seconds = float(f.readline().split()[0])
            day = seconds // (24 * 3600)
            seconds = seconds % (24 * 3600)
            hour = seconds / 3600
            seconds %= 3600
            minutes = seconds //60
            seconds %= 60
            seconds2 = seconds
            timeformat = "d:h:m:s   %d:%d:%d:%d" % (day, hour, minutes, seconds2)
            bot.sendMessage(chat_id, timeformat)
        elif command == '/kodi_on':
            plug_kodi_on_command = "/home/pi/hs100/hs100.sh on -i " +plug_kodi_IP
            print(plug_kodi_on_command)
            os.system(plug_kodi_on_command)
            bot.sendMessage(chat_id, str("Kodi-Steckdose angeschaltet!"))###
        elif command == '/kodi_off':
           kodi_off_command = "ssh "+kodi_IP + " 'shutdown -h now'"
           print(kodi_off_command)
           os.system(kodi_off_command)
           bot.sendMessage(chat_id, str("Kodi shutting down! Wait 15 seconds..."))
           sleep (15)
           plug_kodi_off_command = "/home/pi/hs100/hs100.sh off -i " +plug_kodi_IP
           print(plug_kodi_off_command)
           os.system(plug_kodi_off_command)
           bot.sendMessage(chat_id, str("Kodi-Steckdose aus!"))
        elif command == '/startx':
            os.system('pkill retroarch')
            os.system('pkill emulation*')
            os.system('sudo systemctl start lightdm')
            bot.sendMessage(chat_id, str("startx!"))  
        elif command == '/reboot':
            bot.sendMessage(chat_id, str("rebooting!")) 
            os.system('sudo reboot')
            
            
            
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
