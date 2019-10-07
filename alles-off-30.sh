#!/bin/bash
sleep 900 #15 min
#sleep 10 # 10 sec fuer test
python3 /home/pi/pi-music-bot/volfade.py

pwd
source /home/pi/pi-music-bot/IPs.py

ssh $schlafzi_IP 'sudo shutdown -h now' #schlafzi
ssh $wohnzi_IP 'sudo shutdown -h now' #wohnzi hat nun raspbian drauf!
ssh $kueche_IP 'sudo shutdown -h now' #kueche hat nun raspbian drauf!
sleep 18
/home/pi/hs100/hs100.sh off -i $plug_schlafzi_IP #schlafzi dose
sleep 4
/home/pi/hs100/hs100.sh off -i $plug_kueche_IP #kueche
sleep 1
/home/pi/hs100/hs100.sh off -i $plug_wohnzi_IP #wohnzimmer dose


