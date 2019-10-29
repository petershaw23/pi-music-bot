from time import sleep      # Importing the time library to provide the delays in program
sleep (10)
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

love = datetime.datetime(2019, 5, 26) - datetime.datetime.now()
now = datetime.datetime.now() # Getting date and time
IMG_NAME='none'

def send_image(chat_id,bool):

    img_list=os.listdir('/home/pi/telepot/img/eigene')
    img_name=img_list[random.randint(0,len(img_list)-1)]
    hide_keyboard={'hide_keyboard':True}

    if bool:
        bot.sendPhoto(chat_id,open('/home/pi/telepot/img/eigene/'+img_name, 'rb'),caption=' ',reply_markup=hide_keyboard)
        return


GIF_NAME='none'

def send_gif(chat_id,bool):

    gif_list=os.listdir('/home/pi/telepot/gif/eigene')
    gif_name=gif_list[random.randint(0,len(gif_list)-1)]
    hide_keyboard={'hide_keyboard':True}

    if bool:
        bot.sendVideo(chat_id,open('/home/pi/telepot/gif/eigene/'+gif_name, 'rb'),caption=' ',reply_markup=hide_keyboard)
        return


coffee = '\U00002615'



def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/start':
        bot.sendMessage (chat_id, str("Hi! Dies ist dem Michael sein toller Pi-Bot! Er kann leider nix, aber egal. Versuche mal /roll /time /uptime /date /temp /humidity /pressure oder /meme ! Ausserdem kann er hi sagen :D"))
    elif command == '/time':
        now = datetime.datetime.now() # Getting date and time
        bot.sendMessage(chat_id, str(now.hour) + str(":") + str(now.minute), parse_mode= 'Markdown')
    elif command == '/date':
         now = datetime.datetime.now() # Getting date and time
         bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command in ['hi', 'Hi', 'Hi!', 'hi!']:
        bot.sendMessage (chat_id, str("Selber Hi!"))
    elif command in ['hallo', 'Hallo', 'hallo!', 'Hallo!']:
        bot.sendMessage (chat_id, str("Halloele!"))
    elif command in ['hello', 'Hello', 'hello!', 'Hello!']:
        bot.sendMessage (chat_id, str("helooooooooooooo!"))
    elif command == '/reboot':
        os.system('sudo reboot')


    # RANDOM STUFF
    elif command == '/love':
        now = datetime.datetime.now() # Getting date and time
        love = datetime.datetime(2019, 5, 26) - datetime.datetime.now()
        bot.sendMessage(chat_id, str("\U00002764 noch ") + str(love.days) + str(" Tage! Das sind so viele: ") + str(("\U0001F31E"*love.days)))
    elif command == '/meme':
        send_image(chat_id, True)

    elif command == '/gif':
        send_gif(chat_id, True)

    elif command =='/coffee':
        random_coffee = random.choice(open('/home/pi/telepot/txt/coffee.txt').readlines())+coffee
        bot.sendMessage(chat_id, random_coffee)
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
        bot.sendMessage(chat_id, str("Kodi-Steckdose angeschaltet!"))

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
    
    elif command == '/twitch1':
      os.system('sudo systemctl stop lightdm')
      os.system('pkill retroarch')
      os.system('pkill emulation*')  
      os.system("bash /home/pi/pi-music-bot/twitch1.sh &")
      bot.sendMessage(chat_id, str("snes demo rom 1! twitch.tv/bud_lan_b"))
    
    elif command == '/twitch2':
      os.system('sudo systemctl stop lightdm')
      os.system('pkill retroarch')
      os.system('pkill emulation*')  
      os.system("bash /home/pi/pi-music-bot/twitch2.sh &")
      bot.sendMessage(chat_id, str("snes demo rom 2! watch on twitch.tv/bud_lan_b"))
    
    elif command == '/twitch3':
      os.system('sudo systemctl stop lightdm')
      os.system('pkill retroarch')
      os.system('pkill emulation*')  
      os.system("bash /home/pi/pi-music-bot/twitch3.sh &")
      bot.sendMessage(chat_id, str("genesis demo rom! watch on twitch.tv/bud_lan_b"))
           
    elif command == '/snes':
      os.system('sudo systemctl stop lightdm')
      os.system('pkill retroarch')
      os.system('pkill emulation*')  
      os.system("bash /home/pi/pi-music-bot/snes.sh &")
      bot.sendMessage(chat_id, str("selected snes game started! watch on twitch.tv/bud_lan_b"))
        
    elif command == '/startx':
        os.system('pkill retroarch')
        os.system('pkill emulation*')
        os.system('sudo systemctl start lightdm')
        bot.sendMessage(chat_id, str("startx!"))  
        
    elif command == '/exit':
        os.system('sudo systemctl stop lightdm')
        os.system('pkill retroarch')
        bot.sendMessage(chat_id, str("exit to cli!"))  
 
    
bot = telepot.Bot(token) # get token key from from local file pibot-token.py
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

while 1:
    sleep(10)
