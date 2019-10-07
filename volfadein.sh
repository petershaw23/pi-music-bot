#!/bin/bash
# script to use locally, to fade in after startup. use with "crontab -e" : "@reboot /home/volumio/volfadein.sh"
# don't forget to "sudo chmod +x volfadein.sh" 
sleep 37s
/volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh play
x=25
while [ $x -le 100 ]
do
sleep 3.5s
echo "set value x to: $x"
/volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh volume +$x
x=$(( $x + 1 ))
done
