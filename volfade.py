import time
import os
t = 20 #customize sleep interval
volume = 100 #initial volume

#time.sleep(10) #initial sleep, to let volumio daemon start


while volume > 5:
    volume -=5
    #methode bei local ausfuehrung:
    #os.system("/volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh volume %s" % (volume)
    #methode fuer remote steuerung via rest api/curl:
    os.system("curl http://192.168.0.241/api/v1/commands/?cmd=volume&volume=%s" % (volume))
    print (volume)
    time.sleep(t)
