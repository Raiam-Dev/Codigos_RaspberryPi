from mqtt_config import ClientMqtt
import time

mqtt = ClientMqtt(topico = "acionar/bomba", username = "master", password = "brokerMQ")
mqtt.connectar()

while True:
    time.sleep(1)

