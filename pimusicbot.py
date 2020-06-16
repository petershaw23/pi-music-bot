import time
from time import sleep      # Importing the time library to provide the delays in program
sleep(20)
import sys
import subprocess
from subprocess import Popen, PIPE
import os
import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

import pimusicbot_token # imports local file pibot-token.py with telegram bot token
token = pimusicbot_token.token

#IP Adressen und logins der hs100 steckdosen und raspberry pis aus IPs.py lesen
import IPs
kodi_IP = IPs.kodi_IP
plug_kodi_IP = IPs.plug_kodi_IP

schlafzi_IP = IPs.schlafzi_IP
plug_schlafzi_IP = IPs.plug_schlafzi_IP

wohnzi_IP = IPs.wohnzi_IP
plug_wohnzi_IP = IPs.plug_wohnzi_IP

kueche_IP = IPs.kueche_IP
plug_kueche_IP = IPs.plug_kueche_IP


def on_chat_message(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message


    if command == '/track':
        trackid = subprocess.Popen("curl "+wohnzi_IP+"/api/v1/getstate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (outputRAW, error) = trackid.communicate()
        if trackid.returncode != 0: 
            bot.sendMessage(chat_id, str("Wohnzi aus? Full Error Message: %d %s %s" % (trackid.returncode, outputRAW, error)))
        else: 
            title = outputRAW.decode().split('\"')[9] #curl status string split and select 9th word, which is the track title
            artist = outputRAW.decode().split('\"')[13] #..13th word, is artist
            albumart = outputRAW.decode().split('\"')[21] #.. 21th word, is albumart link
            bot.sendMessage(chat_id, str(albumart))
            bot.sendMessage(chat_id, str(artist)+str(' - ')+str(title))

    elif command == '/dose1':
        dose1 = subprocess.Popen("/home/pi/hs100/hs100.sh -i "+plug_schlafzi_IP+" status", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, error) = dose1.communicate()
        if dose1.returncode != 0:
            bot.sendMessage(chat_id, str("WLAN zu schlecht? Full Error Message: %d %s %s" % (dose1.returncode, output, error)))
        else:
            outputSplit = output.decode().split(',\n')
            bot.sendMessage (chat_id, str(outputSplit[1])+str(outputSplit[18])+str(outputSplit[19]))

    elif command == '/dose2':
        dose2 = subprocess.Popen("/home/pi/hs100/hs100.sh -i "+plug_kueche_IP+" status", stdout=subprocess.PIPE, stderr=subprocess.PIPE,  shell=True)
        (output, error) = dose2.communicate()
        if dose2.returncode != 0:
            bot.sendMessage(chat_id, str("WLAN zu schlecht? Full Error Message: %d %s %s" % (dose2.returncode, output, error)))
        else:
            outputSplit = output.decode().split(',\n')
            bot.sendMessage (chat_id, str(outputSplit[1])+str(outputSplit[18])+str(outputSplit[19]))

    elif command == '/dose3':
        dose3 = subprocess.Popen("/home/pi/hs100/hs100.sh -i "+plug_wohnzi_IP+" status", stdout=subprocess.PIPE, stderr=subprocess.PIPE,  shell=True)
        (output, error) = dose3.communicate()
        if dose3.returncode != 0:
            bot.sendMessage(chat_id, str("WLAN zu schlecht? Full Error Message: %d %s %s" % (dose3.returncode, output, error)))
        else:
            outputSplit = output.decode().split(',\n')
            bot.sendMessage (chat_id, str(outputSplit[1])+str(outputSplit[18])+str(outputSplit[19]))

    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='\U000025B6 play', callback_data='play'), InlineKeyboardButton(text='\U000025FB stop', callback_data='stop'), InlineKeyboardButton(text='\U000023E9 next', callback_data='next')],
                   [InlineKeyboardButton(text='\U0001F4C41', callback_data='playlist1'), InlineKeyboardButton(text='\U0001F4C42', callback_data='playlist2'), InlineKeyboardButton(text='\U0001F4C43', callback_data='playlist3'), InlineKeyboardButton(text='\U0001F4C44', callback_data='playlist4'), InlineKeyboardButton(text='\U0001F4C45', callback_data='playlist5'), InlineKeyboardButton(text='\U0001F4C46', callback_data='playlist6'), InlineKeyboardButton(text='\U0001F4C47', callback_data='playlist7'), InlineKeyboardButton(text='\U0001F4C48', callback_data='playlist8')],
                   [InlineKeyboardButton(text='\U0001F6CF \U0001F50A ', callback_data='schlafzi-on'),
                   InlineKeyboardButton(text='\U0001F374\U0001F50A', callback_data='kueche-on'),
                   InlineKeyboardButton(text='\U0001F6CB \U0001F50A', callback_data='wohnzi-on')],
                   [InlineKeyboardButton(text='\U0001F6CF \U0001F507', callback_data='schlafzi-off'),
                   InlineKeyboardButton(text='\U0001F374\U0001F507', callback_data='kueche-off'),
                   InlineKeyboardButton(text='\U0001F6CB \U0001F507', callback_data='wohnzi-off')],
                   [InlineKeyboardButton(text='\U0001F6CF\U0001F374\U0001F6CB\U0001F507', callback_data='alles-off'),
                   InlineKeyboardButton(text='\U0001F552 t-30', callback_data='alles-off-30'),
                   InlineKeyboardButton(text='\U0001F552 t-45', callback_data='alles-off-45'),
                   InlineKeyboardButton(text='\U0001F552\U0000274C', callback_data='alles-off-cancel')],
               ])

    bot.sendMessage(chat_id, ('Hi! Um den aktuellen Titel zu sehen, gib /track ein!'), reply_markup=keyboard)

def on_callback_query(msg):

    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)



    if query_data == 'play':
        bot.answerCallbackQuery(query_id, text='play')
        print('pressed play')
        os.system('ssh '+kueche_IP+' " mpc volume 80 && mpc play"')
        os.system('ssh '+schlafzi_IP+' " sudo systemctl stop snapclient && omxplayer -o alsa --loop /home/pi/rain.mp3"')
        os.system('ssh '+wohnzi_IP+' " /volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh play"')
        

    elif query_data == 'stop':
        bot.answerCallbackQuery(query_id, text='stop')
        print('pressed stop')
        os.system('ssh '+kueche_IP+' " mpc stop && mpc volume 100"')
        os.system('ssh '+schlafzi_IP+' " killall omxplayer.bin  && sudo systemctl start snapclient"')
        os.system('ssh '+wohnzi_IP+' " /volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh stop"')
        

    elif query_data == 'next':
        bot.answerCallbackQuery(query_id, text='next')
        print('pressed next')
        os.system('ssh '+wohnzi_IP+' " /volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh next"')
        

    elif query_data == 'schlafzi-on':
        bot.answerCallbackQuery(query_id, text='Schlafzimmer angeschaltet!')
        plug_schlafzi_on_command = "/home/pi/hs100/hs100.sh on -i " +plug_schlafzi_IP
        print(plug_schlafzi_on_command)
        os.system(plug_schlafzi_on_command)
        

    elif query_data == 'kueche-on':
        bot.answerCallbackQuery(query_id, text='Kueche angeschaltet!')
        os.system('ssh '+kueche_IP+' " mpc volume 80 && mpc play"')
        plug_kueche_on_command = "/home/pi/hs100/hs100.sh on -i " +plug_kueche_IP
        print(plug_kueche_on_command)
        os.system(plug_kueche_on_command)
        

    elif query_data == 'wohnzi-on':
        bot.answerCallbackQuery(query_id, text='Wohnzimmer angeschaltet!')
        plug_wohnzi_on_command = "/home/pi/hs100/hs100.sh on -i " +plug_wohnzi_IP
        print(plug_wohnzi_on_command)
        os.system(plug_wohnzi_on_command)
        

    elif query_data == 'schlafzi-off':
        bot.answerCallbackQuery(query_id, text='Schlafzimmer aus!')
        os.system('killall alles-off-30.sh') #zuerst evlt  bestehende timer canceln
        os.system('killall alles-off-45.sh') #zuerst evtl bestehende timer canceln
        print('schlafzi pressed off')
        
        os.system('/home/pi/pi-music-bot/schlafzi-off.sh')

    elif query_data == 'kueche-off':
        bot.answerCallbackQuery(query_id, text='Kueche aus!')
        #os.system('killall alles-off-30.sh') #zuerst evlt  bestehende timer canceln
        #os.system('killall alles-off-45.sh') #zuerst evtl bestehende timer canceln
        print('kueche pressed off')
        os.system('/home/pi/pi-music-bot/kueche-off.sh')
        os.system('ssh '+kueche_IP+' " mpc stop"')

    elif query_data == 'wohnzi-off':
        bot.answerCallbackQuery(query_id, text='Wohnzimmer aus!')
        os.system('killall alles-off-30.sh') #zuerst evlt  bestehende timer canceln
        os.system('killall alles-off-45.sh') #zuerst evtl bestehende timer canceln
        print('wohnzi pressed off')
        os.system('/home/pi/pi-music-bot/wohnzi-off.sh')

    elif query_data == 'alles-off':
        print('alles pressed off')
        os.system('killall alles-off-30.sh') #zuerst evlt  bestehende timer canceln
        os.system('killall alles-off-45.sh') #zuerst evtl bestehende timer canceln
        bot.answerCallbackQuery(query_id, text='Alles aus!')
        os.system('/home/pi/pi-music-bot/alles-off.sh')

    elif query_data == 'alles-off-30':
        print('alles30 pressed off')
        os.system('killall alles-off-30.sh') #zuerst evlt  bestehende timer canceln
        os.system('killall alles-off-45.sh') #zuerst evtl bestehende timer canceln
        bot.answerCallbackQuery(query_id, text='Timer 30 min!')
        os.system('/home/pi/pi-music-bot/alles-off-30.sh &')

    elif query_data == 'alles-off-45':
        os.system('killall alles-off-30.sh') #zuerst evlt  bestehende timer canceln
        os.system('killall alles-off-45.sh') #zuerst evtl bestehende timer canceln
        print('alles45 pressed off')
        bot.answerCallbackQuery(query_id, text='Timer 45 min!')
        os.system('/home/pi/pi-music-bot/alles-off-45.sh &')

    elif query_data == 'alles-off-cancel':
        print('alles off canceled')
        bot.answerCallbackQuery(query_id, text='Timer abgebrochen!!')
        os.system('killall alles-off-30.sh')
        os.system('killall alles-off-45.sh')

    elif query_data == 'playlist1':
        print('playlist1 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 1 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist1"')
        
    elif query_data == 'playlist2':
        print('playlist2 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 2 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist2"')
        
    elif query_data == 'playlist3':
        print('playlist2 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 3 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist3"')
        
    elif query_data == 'playlist4':
        print('playlist4 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 4 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist4"')
        
    elif query_data == 'playlist5':
        print('playlist5 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 5 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist5"')
       
    elif query_data == 'playlist6':
        print('playlist6 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 6 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist6"')
        
    elif query_data == 'playlist7':
        print('playlist7 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 7 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist7"')
        
    elif query_data == 'playlist8':
        print('playlist8 pressed')
        bot.answerCallbackQuery(query_id, text='Playlist 8 play!')
        os.system('curl '+wohnzi_IP+'/api/v1/commands/?cmd="playplaylist&name=playlist8"')
        


   # Insert your telegram token below
bot = telepot.Bot(token) #get token from imported file pimusicbot_token.py
print (bot.getMe())
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
