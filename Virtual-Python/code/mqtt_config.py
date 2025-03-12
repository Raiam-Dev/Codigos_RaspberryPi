import json
import sys
sys.path.append("/Mapper/")
sys.path.append("/ComandoPorta/")
import paho.mqtt.client as mqtt
from Mapper import port_mapper_json
from ComandoPorta import port_comand
from Mapper import mapper_return
import time

class ClientMqtt:
    def __init__(self, broker = "192.168.25.104", topico = "meu/topico", port = 1883, client_ip = "192.168.25.104", username = "admin", password = "admin"):
        self.broker = broker
        self.topico = topico
        self.port = port
        self.client_ip = client_ip
        self.username = username
        self.password = password
        self.client = mqtt.Client(client_id = self.client_ip)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect (self, client, userdata, flags, rc):
        try:
            client.subscribe(self.topico)
            print(f"Conectado ao topico {self.topico} com sucesso") 
        except Exception as e:
            print(f"Erro {e} ao se inscrever no topico {self.topico}")

    def on_message (self,client, userdata, msg):
        try:
            msg_json = json.loads(msg.payload.decode())
            
            print(json.dumps(msg_json, indent=4))

            for con in msg_json["comando"]:
                mapper_json = port_mapper_json.MapperPort(
                client_ip = con["client_ip"],
                topico = con["topico"],
                porta = con["porta"],
                estado = con["estado"])

                retorno = mapper_return.MapperReturn(
                    client_ip = mapper_json.client_ip,
                    porta= mapper_json.porta,
                    estado= mapper_json.estado, 
                    topico= mapper_json.topico)
                
                json_retorno = retorno.mapper()
                
                enviar = port_comand.ComandPort(pin=mapper_json.porta, estado=mapper_json.estado)
                enviar.comand()
                time.sleep(1)
                enviar.retornar(msg=json_retorno, topico=retorno.topico)

        except Exception as e:
            print(f"Erro: {e} ao Decodificar a mensagem: {msg_json}")
    
    def on_disconnect (self,client, userdata, rc):
        print(f"Deconectado com Sucesso {rc}")
    
    def publish_msg(self, msg, topico):
        try:
            print("Publicardo")
            self.client.publish(topico, json.dumps(msg))
            print(json.dumps(msg, indent=4))
        except Exception as e:
            print(f"Erro {e} ao enviar a mensagem: {msg} ")

    def connectar(self):
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()