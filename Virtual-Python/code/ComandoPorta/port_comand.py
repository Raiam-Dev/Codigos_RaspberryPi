import sys
sys.path.append("/python3-librpiplc/")
sys.path.append("/code/")
import mqtt_config 
from librpiplc import rpiplc

rpiplc.init("RPIPLC_V6","RPIPLC_58") 

class ComandPort:
    def __init__(self, pin= "", estado = "" ):
        self.pin = pin
        self.estado = estado
        self.enviar = mqtt_config.ClientMqtt("acionar/bomba")
        
    def comand(self):
        rpiplc.pin_mode(self.pin,rpiplc.OUTPUT)
        rpiplc.digital_write(self.pin, self.estado)
    
    def retornar(self, msg, topico):
        self.enviar.publish_msg(msg, topico)

        
