from models.Vagao import Vagao


class Transporte:

    def __init__(self, listaCameras: list[Vagao], urlArduino: str, limite: int):
        self.__listaCameras = listaCameras
        self.__urlArduino = urlArduino
        self.__limite = limite

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])

    @property
    def listaVagoes(self):
        return self.__listaVagoes

    @listaVagoes.setter
    def listaVagoes(self, nova_listaVagoes: list[Vagao]):
        self.__listaVagoes = nova_listaVagoes

    @property
    def urlArduino(self):
        return self.__urlArduino

    @urlArduino.setter
    def urlArduino(self, nova_urlArduino: str):
        self.__urlArduino = nova_urlArduino

    @property
    def limite(self):
        return self.__limite

    @limite.setter
    def limite(self, nova_limite: int):
        self.__limite = nova_limite
