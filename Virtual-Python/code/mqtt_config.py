import json
import sys
import time
sys.path.append("/Mapper/")
sys.path.append("/ComandoPorta/")
from dto import json_deserializer
from dto import json_serializer
from Transmiter import rasp_transmiter
import paho.mqtt.client as mqtt

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
            json_dicionario = json.loads(msg.payload.decode())
            
            print(json.dumps(json_dicionario, indent=4))

            for json_info in json_dicionario["comando"]:
                json_decoder = json_deserializer.JsonDeserializer(
                client_ip = json_info["client_ip"],
                topico = json_info["topico"],
                porta = json_info["porta"],
                estado = json_info["estado"])

                info_json = json_serializer.JsonSerializer(
                    client_ip = json_decoder.client_ip,
                    porta= json_decoder.porta,
                    estado= json_decoder.estado, 
                    topico= json_decoder.topico)
                
                json_retorno = info_json.Json()
                
                enviar = rasp_transmiter.RaspTransmiter(pin=info_json.porta, estado=info_json.estado)
                enviar.envio()
                enviar.resposta(msg=json_retorno, topico=info_json.topico)
        except Exception as e:
            print(f"Erro: {e} ao Decodificar a mensagem: {info_json}")
    
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