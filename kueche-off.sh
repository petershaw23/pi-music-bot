#!/bin/bash
pwd
source /home/pi/pi-music-bot/IPs.py
ssh $kueche_IP 'sudo shutdown -h now'
sleep 20
/home/pi/hs100/hs100.sh off -i $plug_kueche_IP #kueche



