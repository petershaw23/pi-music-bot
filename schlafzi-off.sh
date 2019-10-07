#!/bin/bash

pwd
source /home/pi/pi-music-bot/IPs.py
ssh $schlafzi_IP 'sudo shutdown -h now'
sleep 18
/home/pi/hs100/hs100.sh off -i $plug_schlafzi_IP
