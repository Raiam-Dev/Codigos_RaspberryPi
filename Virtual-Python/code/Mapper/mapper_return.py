class MapperReturn:
    def __init__(self, client_ip = "0", porta = "0", estado = "0", topico = "receber/rx"):
        self.client_ip = client_ip
        self.porta = porta
        self.estado = estado
        self.topico = topico

    def mapper(self):
        return {
            "topico": self.topico,
            "client_ip": self.client_ip,
            "porta": self.porta,
            "estado": self.estado,
        }