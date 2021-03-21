from models.Vagao import Vagao


class Transporte:

    def __init__(self, listaCameras: list[Vagao], urlArduino: str):
        self.__listaCameras = listaCameras
        self.__urlArduino = urlArduino

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
